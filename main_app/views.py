from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cat
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

# Define the index view
def cats_index(request):
    cats = Cat.objects.all()
    # Handles the request, points to the template to render, and we are providing a dict with a cats key which has a value of all the cats
    return render(request, 'cats/index.html', { 'cats': cats })

# Define the detail view
def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {'cat': cat, 'feeding_form': feeding_form})

class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    # Special string pattern Django will use
    # success_url = '/cats/{cat_id}' <- what it may look like under hood
    # Or if you wanted to redirect to the index page
    # success_url = '/cats'

class CatUpdate(UpdateView):
  model = Cat
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats'
