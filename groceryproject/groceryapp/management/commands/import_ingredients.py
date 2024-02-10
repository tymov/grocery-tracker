import os
import json
from django.core.management.base import BaseCommand
from groceryapp.models import Ingredient

class Command(BaseCommand):
    help = 'Import ingredients from JSON file'

    def handle(self, *args, **kwargs):
        # Get absolute path to the JSON file
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'filtered_food_items.json')
        
        # Open JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract food items from JSON data
        food_items = data["food_items"]

        # Create ingredients in the database
        for item in food_items:
            Ingredient.objects.get_or_create(name=item)
        
        self.stdout.write(self.style.SUCCESS('Successfully imported ingredients'))
