from django.db import models

# Create your models here.
## CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

## ITEM
class GroceryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expiration_date = models.DateTimeField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=None)
    location = models.CharField(max_length=100)
    unit_of_measure = models.CharField(max_length=100, null=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return f"{self.name} - Quantity: {self.quantity}"
    
## RECIPE
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.ManyToManyField(GroceryItem, related_name='recipes')
    instructions = models.TextField()

    def __str__(self):
        return self.name
