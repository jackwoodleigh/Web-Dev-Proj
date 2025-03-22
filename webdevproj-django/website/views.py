from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RecipeForm
from .models import Recipe
from django.core.paginator import Paginator

def home(request):
    #featured_recipes = Recipe.objects.filter(featured=True)
    #popular_recipes = Recipe.objects.filter(popular=True)
    context = {
        #'featured_recipes': featured_recipes,
        #'popular_recipes': popular_recipes,
    }
    return render(request, 'home.html', context)

def recipe(request):
    return render(request, 'recipe.html')

def submit_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = RecipeForm()
    return render(request, 'submit_recipe.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def recipe_list(request):
    return render(request, 'recipe_list.html')


def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-id')
    paginator = Paginator(recipes, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'recipe_list.html', {'page_obj': page_obj})


