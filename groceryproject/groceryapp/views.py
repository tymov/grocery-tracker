from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from .forms import *
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Subquery, OuterRef
from django.db.models import Q
from django.db import connection
import re

# Login / Logout / Register / Password Reset
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return redirect('items')
            else:
                return HttpResponse('Invalid credentials')

    else:
        form = LoginForm()
    return render(request, 'groceryapp/login.html', {'form': form})


# Create your views here.
@login_required
def index(request):    
    # get recipes
    recipes = Recipe.objects.all()
    
    # feature recipes (5 random recipes)
    feature_recipes1 = Recipe.objects.order_by('?')[:4]
    feature_recipes2 = Recipe.objects.order_by('?')[:4]
    feature_recipes3 = Recipe.objects.order_by('?')[:4]
    
    return render(request, 'groceryapp/index.html', {'feature_recipes1': feature_recipes1, 'feature_recipes2': feature_recipes2, 'feature_recipes3': feature_recipes3, 'recipes': recipes})

@login_required
def items(request):
    # Filter items based on the currently logged-in user
    items = GroceryItem.objects.filter(owner=request.user)
    categories = Category.objects.all()
    
    item_name = request.GET.get('item_name')
    if item_name:
        items = items.filter(name__icontains=item_name)
        
    return render(request, 'groceryapp/items.html', {'items': items, 'categories': categories})

@login_required
def recipes(request):
    recipes = Recipe.objects.all()
    
    recipe_name = request.GET.get('recipe_name', '')
    if recipe_name:
        recipes = recipes.filter(name__icontains=recipe_name)
        
    # Get distinct cuisine values from the Recipe model
    cuisines = Recipe.objects.values_list('cuisine', flat=True).distinct()
    
    return render(request, 'groceryapp/recipes.html', {'recipes': recipes, 'cuisines': cuisines})



@login_required
def recipe_detail(request, id):
    # Fetch the recipe and ingredients
    recipe = Recipe.objects.get(id=id)
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    # Format the instructions string by inserting a newline character after each number followed by a period
    formatted_instructions = re.sub(r'(\d+\.)', r'\1\n', recipe.instructions)

    # Pass the formatted instructions to the template
    return render(request, 'groceryapp/recipe_detail.html', {
        'recipe': recipe,
        'recipe_ingredients': recipe_ingredients,
        'formatted_instructions': formatted_instructions
    })
    
@login_required
def addItem(request):
    if request.method == "POST":
        form = GroceryItemForm(request.POST)
        if form.is_valid():
            # Set the owner of the item to the currently logged-in user
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect('items')
    else:
        form = GroceryItemForm()
    return render(request, 'groceryapp/addItem.html', {'form': form})

@login_required
def addRecipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # Associate the logged-in user with the recipe
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            return redirect('recipes')
    else:
        form = RecipeForm()
    return render(request, 'groceryapp/addRecipe.html', {'form': form})

@login_required
def editItem(request, id):
    item = get_object_or_404(GroceryItem, id=id, owner=request.user)
    if request.method == "POST":
        form = GroceryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items')
    else:
        form = GroceryItemForm(instance=item)
    return render(request, 'groceryapp/editItem.html', {'form': form, 'item': item})

@login_required
def editRecipe(request, id):
    recipe = Recipe.objects.get(id=id)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipes')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'groceryapp/editRecipe.html', {'form': form})

@login_required
def deleteItem(request, id):
    item = get_object_or_404(GroceryItem, id=id, owner=request.user)
    item.delete()
    return redirect('items')

@login_required
def deleteRecipe(request, id):
    recipe = Recipe.objects.get(id=id)
    recipe.delete()
    return redirect('recipes')

@login_required
def increment_quantity(request, item_id):
    item = get_object_or_404(GroceryItem, pk=item_id)
    item.quantity += 1
    item.save()
    return JsonResponse({'quantity': item.quantity})

@login_required
def decrement_quantity(request, item_id):
    item = get_object_or_404(GroceryItem, pk=item_id)
    if item.quantity > 0:
        item.quantity -= 1
        item.save()
    return JsonResponse({'quantity': item.quantity})

@login_required
def addIngredients(request, id):
    # Ensure the recipe exists and the user is the owner
    recipe = get_object_or_404(Recipe, id=id, owner=request.user)
    IngredientFormSet = formset_factory(RecipeIngredientForm, extra=10)  # Change 'extra' to  10
    
    if request.method == "POST":
        formset = IngredientFormSet(request.POST, prefix='ingredients')
        if formset.is_valid():
            for form in formset:
                if form.has_changed() and all([field.value() is not None for field in form]):
                    instance = form.save(commit=False)
                    instance.recipe = recipe
                    instance.save()
            return redirect('recipes')
    else:
        formset = IngredientFormSet(prefix='ingredients')
    
    return render(request, 'groceryapp/addIngredients.html', {'formset': formset, 'recipe': recipe})

@login_required
def filter_recipes(request):
    # Get the user's grocery items names and convert to lowercase
    items = [item.lower() for item in GroceryItem.objects.filter(owner=request.user).values_list('name', flat=True)]

    # Get all the recipes and their ingredients
    recipes = Recipe.objects.all()
    recipe_ingredients = RecipeIngredient.objects.all()
    
    # Create a dictionary to store the recipes that can be made with the user's grocery items
    recipes_dict = {}
    for recipe in recipes:
        recipes_dict[recipe.name] = []
        for ingredient in recipe_ingredients:
            if ingredient.recipe == recipe:
                # Convert the ingredient name to lowercase for comparison
                recipes_dict[recipe.name].append(ingredient.ingredient.name.lower())
                
    # Create a list of recipes that can be made with the user's grocery items
    recipes_list = []
    for recipe, ingredients in recipes_dict.items():
        if all(ingredient in items for ingredient in ingredients):
            recipes_list.append(recipe)
            
    # Get the recipes that can be made with the user's grocery items
    recipes = Recipe.objects.filter(name__in=recipes_list)
    
    return render(request, 'groceryapp/recipes.html', {'recipes': recipes})
