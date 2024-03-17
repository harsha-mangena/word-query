from django.urls import path, include
from . import views

urlpatterns = [
    path('random', views.get_random_word_for_day, name='random_word'),
    path('search',views.search_words, name='search_words')
]