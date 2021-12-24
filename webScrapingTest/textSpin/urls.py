from django.urls import path
from .views import articleScrapingView

urlpatterns = [
    path('scraping/', articleScrapingView, name='index')
]