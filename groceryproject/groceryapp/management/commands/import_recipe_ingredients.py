import os
import json
from django.core.management.base import BaseCommand
from groceryapp.models import Recipe, GroceryItem, RecipeIngredient

class Command(BaseCommand):
    help = 'Import recipe ingredients from JSON file'

    def handle(self, *args, **kwargs):
        # Get absolute path to the JSON file
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipe_ingredients.json')
        
        # Open JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract recipe ingredients from JSON data
        recipe_ingredients = data.get("recipe_ingredients", [])

        # Create recipe ingredients in the database
        for recipe_ingredient_data in recipe_ingredients:
            recipe_name = recipe_ingredient_data.pop("recipe")
            ingredient_name = recipe_ingredient_data.pop("ingredient")
            amount = recipe_ingredient_data.pop("amount")
            
            # Get or create Recipe object
            recipe, _ = Recipe.objects.get_or_create(name=recipe_name)
            
            # Get or create GroceryItem object
            grocery_item, _ = GroceryItem.objects.get_or_create(name=ingredient_name)
            
            # Create RecipeIngredient object
            RecipeIngredient.objects.create(recipe=recipe, ingredient=grocery_item, amount=amount)
        
        self.stdout.write(self.style.SUCCESS('Successfully imported recipe ingredients'))
