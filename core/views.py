from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import random
from django.core.cache import cache
from utils import get_query_set, get_word_query_set, get_cached_word_count, check_rate_limit
from .serializer import WordSerializer
from .models import Word


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_random_word_api(request):
    # if not check_rate_limit(request, 'get_random_word_api'):
    #     return Response({"error": "Rate limit exceeded."}, status=429)

    count = get_cached_word_count()
    random_index = random.randint(0, count - 1)
    random_word = get_query_set()[random_index]

    if not random_word:
        return Response({"error": "No words available"}, status=404)

    serializer = WordSerializer(random_word)
    return Response(serializer.data)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_word_for_day(request):
    """
    Get a random word for the day.
    """
    # if not check_rate_limit(request, 'get_word_for_day'):
    #     return Response({"error": "Rate limit exceeded."}, status=429)

    word_of_the_day = cache.get('word_of_the_day')
    if not word_of_the_day:
        count = get_cached_word_count()
        random_index = random.randint(0, count - 1)
        word_of_the_day = get_query_set()[random_index]
        if word_of_the_day is None:
            return Response({"error": "Word not found"}, status=404)

        cache.set('word_of_the_day', word_of_the_day, timeout=86400)

    serializer = WordSerializer(word_of_the_day)
    return Response(serializer.data)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_searched_words_api(request):
    if not check_rate_limit(request, 'get_searched_words_api'):
        return Response({"error": "Rate limit exceeded."}, status=429)

    serialized_data = get_word_query_set(request)
    return Response(serialized_data)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_words_by_length_api(request):
    # if not check_rate_limit(request, 'get_words_by_length_api'):
    #     return Response({"error": "Rate limit exceeded."}, status=429)

    length = request.GET.get('len', None)
    if length is not None:
        try:
            length = int(length)
            filtered_words = Word.objects.filter(length=length)[:25]
            serializer = WordSerializer(filtered_words, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid length provided."}, status=400)
    else:
        return Response({"error": "Length parameter is required."}, status=400)
