from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Cat

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
    return render(request, 'cats/detail.html', {'cat': cat})

class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    # Special string pattern Django will use
    # success_url = '/cats/{cat_id}' <- what it may look like under hood
    # Or if you wanted to redirect to the index page
    # success_url = '/cats'