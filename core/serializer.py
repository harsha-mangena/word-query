from .models import Word
from rest_framework import serializers

class WordSerializer(serializers.ModelSerializer):
    word = serializers.CharField(required=True)
    definition = serializers.JSONField()
    is_popular_now = serializers.BooleanField()

    class Meta:
        model = Word
        fields = ['word', 'definition', 'is_popular_now']