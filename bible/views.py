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

    def post(self, request):
        try:
            user_message = request.data.get("message")  # 일반 텍스트 메시지 받기
            if not user_message:
                return Response({"error": "message 데이터가 없습니다."}, status=400)

            response = self.get_llama_response(user_message)
            return Response({"response": response})

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def get_llama_response(self, user_message):
        llama_api_url = "http://localhost:8080/completion"
        headers = {
            "Content-Type": "application/json"
        }

        # 사용자 메시지 그대로 사용
        prompt = user_message

        data = {
            "prompt": prompt,
            "n_predict": 128
        }

        response = requests.post(llama_api_url, json=data, headers=headers)

        if response.status_code == 200:
            llama_data = response.json()
            return llama_data.get('content', "응답 없음")
        else:
            return "챗봇 응답에 실패했습니다."