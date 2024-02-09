from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    return render(request, 'groceryapp/recipes.html', {'recipes': recipes})

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
        form = RecipeForm(request.POST)
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
def update_loss_graph(request, item_id):
    # Your logic to update the loss graph
    # Example:
    try:
        item = GroceryItem.objects.get(pk=item_id)
        # Update the loss graph based on the item's category, quantity, and price
        # Your logic here
        return JsonResponse({'success': True})
    except GroceryItem.DoesNotExist:
        return JsonResponse({'success': False}, status=404)