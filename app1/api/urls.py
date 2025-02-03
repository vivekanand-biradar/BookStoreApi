from django.urls import path,include
from app1.api import views
from rest_framework.routers import DefaultRouter



# Creating router
router = DefaultRouter()

# Registering all views with router
router.register('AuthorAPI', views.AuthorModelViewSet, basename='author')
router.register('BookAPI', views.BookModelViewSet, basename='book')
router.register('GenreAPI', views.GenreModelViewSet, basename='genre')
router.register('PurchaseAPI', views.PurchaseModelViewSet, basename='purchase')
router.register('ReviewAPI', views.ReviewModelViewSet, basename='Review')

urlpatterns = [
    path('',include(router.urls)),
    path('auth/',include('rest_framework.urls'))
]