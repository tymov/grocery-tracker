import os
import json
from django.core.management.base import BaseCommand
from groceryapp.models import Recipe, GroceryItem, RecipeIngredient

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
            # Create recipe
            recipe = Recipe.objects.create(
                name=recipe_data.get("name", ""),
                description=recipe_data.get("description", ""),
                image=recipe_data.get("image", ""),
                mealtype=recipe_data.get("mealtype", ""),
                time=recipe_data.get("time", ""),
                portions=recipe_data.get("portions", 1),
                instructions=recipe_data.get("instructions", "")
            )
            
            # Create ingredients for the recipe
            ingredients_data = recipe_data.get("ingredients", [])
            for ingredient_data in ingredients_data:
                ingredient_name = ingredient_data.get("name", "")
                quantity = ingredient_data.get("quantity", 1)
                unit_of_measure = ingredient_data.get("unit_of_measure", "")
                
                # Get or create ingredient
                ingredient, _ = GroceryItem.objects.get_or_create(name=ingredient_name)
                
                # Create recipe-ingredient relationship
                RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=f"{quantity} {unit_of_measure}")

        self.stdout.write(self.style.SUCCESS('Successfully imported recipes'))
