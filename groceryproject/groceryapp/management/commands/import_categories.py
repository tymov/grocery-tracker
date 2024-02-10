import os
import json
from django.core.management.base import BaseCommand
from groceryapp.models import Recipe, GroceryItem

class Command(BaseCommand):
    help = 'Import recipes from JSON file'

    def handle(self, *args, **kwargs):
        # Get absolute path to the JSON file
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipes.json')
        
        # Open JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract recipes from JSON data
        recipes = data.get("recipes", [])

        # Create recipes in the database
        for recipe_data in recipes:
            ingredients_data = recipe_data.pop("ingredients", [])
            recipe = Recipe.objects.create(**recipe_data)
            for ingredient_data in ingredients_data:
                item_name = ingredient_data.pop("name")
                grocery_item, _ = GroceryItem.objects.get_or_create(name=item_name)
                recipe.ingredients.add(grocery_item)
        
        self.stdout.write(self.style.SUCCESS('Successfully imported recipes'))
