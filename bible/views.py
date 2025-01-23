from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BibleVerse
from .serializers import BibleVerseSerializer

class BibleVerseView(APIView):
    def get(self, request, book, chapter, verse):
        try:
            verse = BibleVerse.objects.get(book=book, chapter=chapter, verse=verse)
            serializer = BibleVerseSerializer(verse)
            return Response(serializer.data)
        except BibleVerse.DoesNotExist:
            return Response({"error": "Verse not found"}, status=404)
