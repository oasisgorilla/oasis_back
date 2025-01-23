from rest_framework import serializers
from .models import BibleVerse

class BibleVerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleVerse
        fields = '__all__'