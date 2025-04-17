import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BibleVerse
from .serializers import BibleVerseSerializer
import urllib.parse

class BibleChapterView(APIView):
    def get(self, request, book, chapter, start_verse=None, end_verse=None):
        # URL 디코딩 (공백, 특수문자 처리)
        book = urllib.parse.unquote(book)
        
        try:
            # start_verse와 end_verse가 없는 경우, 해당 장(chapter)의 모든 구절 조회
            if start_verse is None or end_verse is None:
                verses = BibleVerse.objects.filter(book=book, chapter=chapter).order_by("verse")
            else:
                verses = BibleVerse.objects.filter(
                    book=book, chapter=chapter, verse__gte=start_verse, verse__lte=end_verse
                ).order_by("verse")
            
            if not verses.exists():
                return Response({"error": "Verses not found"}, status=404)

            serializer = BibleVerseSerializer(verses, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class LlamaChatView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "Prompt is required."}, status=400)

        llama_api_url = "http://localhost:8080/completion"
        headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "identity"  # gzip 비활성화
        }
        data = {
            "prompt": prompt,
            "n_predict": 128
        }

        try:
            response = requests.post(llama_api_url, json=data, headers=headers)
            llama_data = response.json()
            return Response({"reply": llama_data.get("content", "No response from Llama.")})
        except Exception as e:
            print("🔥 Llama API Error:", str(e))  # 콘솔 로그 출력
            return Response({"error": str(e)}, status=500)