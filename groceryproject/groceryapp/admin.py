from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(GroceryItem)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)