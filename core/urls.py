from django.urls import path, include
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('words/random', views.get_random_word_for_day, name='random_word'),
    path('words/search', views.search_words, name='search_words'),
    path('api/words', views.search_words, name='api_search_words'),
]
