from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .serializer import WordSerializer
from .models import Word
import random

@api_view(['GET'])
def get_random_word_for_day(request):
    count = Word.objects.count()
    if count == 0:
        return Response({'error': 'No words available'}, status=404)
    random_index = random.randint(0, count - 1)
    random_word = Word.objects.all()[random_index]
    serializer = WordSerializer(random_word)
    return Response(serializer.data)

@api_view(['GET'])
def search_words(request):
    search_term = request.GET.get('q', '')
    search_type = request.GET.get('type', 'both')
    sort_order = '-' if request.GET.get('sort', '1') == '-1' else ''

    query_set = Word.objects.all()

    if search_type in ['word', 'both']:
        query_set = query_set.filter(word__icontains=search_term)
    if search_type in ['definition', 'both']:
        query_set = query_set.filter(definition__icontains=search_term)

    results = query_set.order_by(f"{sort_order}word")[:50]

    serializer = WordSerializer(results, many=True)
    return Response(serializer.data)
