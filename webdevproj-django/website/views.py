from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RecipeForm

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


