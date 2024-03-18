from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from utils import get_word_query_set
from .serializer import WordSerializer
from .models import Word
import random
from django.core.cache import cache

@api_view(['GET'])
def get_random_word_for_day(request):
    word_of_the_day = cache.get('word_of_the_day')

    if not word_of_the_day:
        count = Word.objects.count()
        if count == 0:
            return Response({'error': 'No words available'}, status=404)

        random_index = random.randint(0, count - 1)
        random_word = Word.objects.all()[random_index]
        random_word.count += 1  
        random_word.save(update_fields=['count'])
        cache.set('word_of_the_day', random_word, timeout=86400)
    else:
        random_word = Word.objects.get(id=word_of_the_day.id)  # Ensure we have the latest instance

    serializer = WordSerializer(random_word)
    return Response(serializer.data)

@api_view(['GET'])
def search_words(request):
    serialized_data = get_word_query_set(request)
    return Response(serialized_data.data)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_searched_words(request):
    serialized_data = get_word_query_set(request)
    return Response(serialized_data.data)
    