from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expiration_date = models.DateTimeField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=None)
    location = models.CharField(max_length=100)
    unit_of_measure = models.CharField(max_length=100, null=True, default=None)
    notes = models.TextField(null=True, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Add this line
    date_bought = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image = models.URLField(default='https://example.com/default-image.jpg')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')
    mealtype = models.TextField(null=True)
    time = models.CharField(max_length=100, null=True)
    portions = models.IntegerField(null=True)
    instructions = models.TextField(null=True)
    cuisine = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.recipe} - {self.ingredient} - {self.amount}"
