from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, 'users')
router_v1.register('tags', TagViewSet, 'tags')
router_v1.register('ingredients', IngredientViewSet, 'ingredients')
router_v1.register('recipes', RecipeViewSet, 'recipes')


urlpatterns = (
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
)
