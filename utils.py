from core.models import Word
from core.serializer import WordSerializer
from django.db.models import Q

def get_word_query_set(request):
    search_term = request.GET.get('q', '')
    search_type = request.GET.get('type', 'both')
    sort_order = '-' if request.GET.get('sort', '1') == '-1' else ''
    order_by = f"{sort_order}word"

    query_set = Word.objects.all()

    if search_type == 'word':
        query_set = query_set.filter(word__icontains=search_term)
    elif search_type == 'definition':
        query_set = query_set.filter(definition__icontains=search_term)
    elif search_type == 'both':
        query_set = query_set.filter(Q(word__icontains=search_term) | Q(definition__icontains=search_term))

    results = query_set.order_by(order_by)[:50]

    serializer = WordSerializer(results, many=True)
    return serializer