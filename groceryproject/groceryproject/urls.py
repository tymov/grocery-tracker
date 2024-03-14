"""
URL configuration for groceryproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from groceryapp import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('items/', views.items, name='items'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipe_detail/<int:id>', views.recipe_detail, name='recipe_detail'),
    path('items/addItem/', views.addItem, name='addItem'),
    path('recipes/addRecipe/', views.addRecipe, name='addRecipe'),
    path('items/editItem/<int:id>', views.editItem, name='editItem'),
    path('recipes/editRecipe/<int:id>', views.editRecipe, name='editRecipe'),
    path('items/deleteItem/<int:id>', views.deleteItem, name='deleteItem'),
    path('recipes/deleteRecipe/<int:id>', views.deleteRecipe, name='deleteRecipe'),
    path('recipe/addIngredient/<int:id>', views.addIngredients, name='addIngredients'),
    path('recipe/editIngredient/<int:id>', views.editIngredient, name='editIngredient'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    # path('register/', views.register, name='register'),
    # path('password_reset/', views.password_reset, name='password_reset'),
    path('decrement_quantity/<int:item_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('increment_quantity/<int:item_id>/', views.increment_quantity, name='increment_quantity'),
    path('recipe/filter/', views.filter_recipes, name='filter_recipes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   
