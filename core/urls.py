from django.urls import path, include
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('word/random', views.get_random_word_api, name='random_word'),
    path('word/day', views.get_word_for_day, name='search_words'),
    path('word/search', views.get_searched_words_api, name='api_search_words'),
    path('word/length', views.get_words_by_length_api, name='words_by_length')
]
