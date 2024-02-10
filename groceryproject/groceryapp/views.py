from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from .forms import *
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

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
    return render(request, 'groceryapp/index.html')

@login_required
def items(request):
    items = GroceryItem.objects.all()
    categories = Category.objects.all()
    
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        items = items.filter(name__icontains=item_name)
        
    return render(request, 'groceryapp/items.html', {'items': items, 'categories': categories})

@login_required
def recipes(request):
    recipes = Recipe.objects.all()
    
    # Get all grocery items that exist in the database and convert to lowercase
    existing_grocery_items = GroceryItem.objects.all().values_list('name', flat=True)
    existing_grocery_items_list = [item.lower() for item in existing_grocery_items]
    print("Existing Grocery Items:", existing_grocery_items_list)
        
    # Get the IDs of recipes containing any of the grocery items
    recipe_ids = RecipeIngredient.objects.filter(ingredient__name__in=existing_grocery_items_list).values_list('recipe', flat=True).distinct()
    print("Recipe IDs:", recipe_ids)
        
    # Fetch the recipes that have matching ingredients
    recipes = Recipe.objects.filter(id__in=recipe_ids)
    
    recipe_name = request.GET.get('recipe_name')
    if recipe_name != '' and recipe_name is not None:
        recipes = recipes.filter(name__icontains=recipe_name)
        
    return render(request, 'groceryapp/recipes.html', {'recipes': recipes})

@login_required
def recipe_detail(request, id):
    recipe = Recipe.objects.get(id=id)
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    return render(request, 'groceryapp/recipe_detail.html', {'recipe': recipe, 'recipe_ingredients': recipe_ingredients})

@login_required
def addItem(request):
    if request.method == "POST":
        form = GroceryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items')
    else:
        form = GroceryItemForm()
    return render(request, 'groceryapp/addItem.html', {'form': form})

@login_required
def addRecipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes')
    else:
        form = RecipeForm()
    return render(request, 'groceryapp/addRecipe.html', {'form': form})

@login_required
def editItem(request, id):
    item = GroceryItem.objects.get(id=id)
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
    item = GroceryItem.objects.get(id=id)
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
    recipe = Recipe.objects.get(id=id)
    IngredientFormSet = formset_factory(RecipeIngredientForm, extra=5)  # Adjust 'extra' as needed
    
    if request.method == "POST":
        formset = IngredientFormSet(request.POST, prefix='ingredients')
        if formset.is_valid():
            for form in formset:
                instance = form.save(commit=False)
                instance.recipe = recipe
                instance.save()
            return redirect('recipes')
    else:
        formset = IngredientFormSet(prefix='ingredients')
    
    return render(request, 'groceryapp/addIngredients.html', {'formset': formset, 'recipe': recipe})
