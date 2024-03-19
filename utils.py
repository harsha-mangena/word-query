from core.models import Word
from core.serializer import WordSerializer
from django.db.models import Q
from django.core.cache import cache


def get_query_set():
    qs = cache.get('query_set')
    if qs is None:
        qs = Word.objects.all()
        cache.set('query_set', qs, timeout=86400)
    return qs


def construct_search_query(search_term, search_type='both'):
    """
    Constructs a Q object based on the search term and search type.
    """
    if search_type == 'word':
        return Q(word__icontains=search_term)
    elif search_type == 'definition':
        return Q(definition__icontains=search_term)
    return Q(word__icontains=search_term) | Q(definition__icontains=search_term)


def get_word_query_set(request):
    search_term = request.GET.get('q', '')
    search_type = request.GET.get('type', 'both')
    sort_order = '-' if request.GET.get('sort', '1') == '-1' else ''
    order_by = f"{sort_order}word"

    search_query = construct_search_query(search_term, search_type)
    query_set = Word.objects.filter(search_query).order_by(order_by)[:50]

    serializer = WordSerializer(query_set, many=True)
    return serializer


def get_cached_word_count():
    count = cache.get('cached_word_count')
    if count is None:
        count = Word.objects.count()
        cache.set('cached_word_count', count, timeout=3600)
    return count


def check_rate_limit(request, key_prefix, limit=10, period=60):
    user_ip = request.META.get('REMOTE_ADDR', '')
    key = f"{key_prefix}_{user_ip}"
    request_count = cache.get(key, 0)
    if request_count >= limit:
        return False
    else:
        cache.set(key, request_count + 1, timeout=period)
        return True
