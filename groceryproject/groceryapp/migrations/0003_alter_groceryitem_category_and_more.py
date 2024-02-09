# Generated by Django 4.2.9 on 2024-02-08 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groceryapp', '0002_alter_groceryitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groceryitem',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groceryapp.category'),
        ),
        migrations.AlterField(
            model_name='groceryitem',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='groceryitem',
            name='expiration_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='groceryitem',
            name='notes',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='groceryitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='groceryitem',
            name='unit_of_measure',
            field=models.CharField(max_length=100, null=True),
        ),
    ]