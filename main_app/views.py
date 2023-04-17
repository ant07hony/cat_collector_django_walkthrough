import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cat, Toy, Photo
from .forms import FeedingForm

# cats = [
#   {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
# ]

# Create your views here.
def home(request):
    return render(request, 'home.html')

# Define the about view
def about(request):
    return render(request, 'about.html')

@login_required
# Define the index view
def cats_index(request):
    #cats = Cat.objects.all() <- shows all cats all the time
    cats = Cat.objects.filter(user=request.user) #<- shows only cats specific to user when logged
    # Handles the request, points to the template to render, and we are providing a dict with a cats key which has a value of all the cats
    return render(request, 'cats/index.html', { 'cats': cats })

@login_required
# Define the detail view
def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    id_list = cat.toys.all().values_list('id')
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {'cat': cat, 'feeding_form': feeding_form, 'toys': toys_cat_doesnt_have})


@login_required
def add_feeding(request, cat_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('detail', cat_id=cat_id)


@login_required
def assoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('detail', cat_id=cat_id)
 

@login_required
def add_photo(request, cat_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, cat_id=cat_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', cat_id=cat_id)
  
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
       

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # Special string pattern Django will use
    # success_url = '/cats/{cat_id}' <- what it may look like under hood
    # Or if you wanted to redirect to the index page
    # success_url = '/cats'
    
    # This inherited method is called when a
    # valid cat form is being submitted
    def form_valid(self, form):
      # Assign the logged in user (self.request.user)
      form.instance.user = self.request.user
      # form.instance is the cat
      # Let the CreateView do its job as usual
      return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
  model = Cat
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
  model = Cat
  success_url = '/cats'
