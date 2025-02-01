from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BibleVerse
from .serializers import BibleVerseSerializer
import urllib.parse

class BibleVerseView(APIView):
    def get(self, request, book, chapter, verse):
        book = urllib.parse.unquote(book) # 1%20Samuel 과 같이 오는 요청에서 공백 제거
        print(book)
        try:
            verse = BibleVerse.objects.get(book=book, chapter=chapter, verse=verse)
            serializer = BibleVerseSerializer(verse)
            return Response(serializer.data)
        except BibleVerse.DoesNotExist:
            return Response({"error": "Verse not found"}, status=404)
