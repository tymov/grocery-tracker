# Generated by Django 4.2.9 on 2024-02-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceryapp', '0002_alter_recipe_mealtype_delete_mealtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='recipe_images/'),
        ),
    ]
