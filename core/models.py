from django.db import models
from django.utils import timezone

class Word(models.Model):
    word = models.CharField(max_length=100, unique=True)
    definition = models.TextField()
    count = models.IntegerField(default=0)  
    pos = models.CharField(max_length=50, blank=True, null=True) 
    is_popular_now = models.BooleanField(default=False)
    popularity_updated_at = models.DateTimeField(default=timezone.now)