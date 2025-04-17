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
            # 프론트엔드에서 보낸 'prompt' 필드를 받아옵니다
            prompt = request.data.get('prompt')
            if not prompt:
                return Response({"error": "prompt field is required"}, status=400)

            # llama.cpp API로 요청 보내기
            llama_api_url = "http://localhost:8080/completion"  # llama.cpp가 실행 중인 URL
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "prompt": prompt,
                "n_predict": 128  # 예시로 예측 토큰 수를 설정, 필요에 맞게 조정
            }

            # llama.cpp 서버로 POST 요청 보내기
            response = requests.post(llama_api_url, json=data, headers=headers)

            if response.status_code == 200:
                llama_data = response.json()
                return Response({"reply": llama_data.get('content', "챗봇 응답에 실패했습니다.")})
            else:
                return Response({"error": "Failed to get response from llama.cpp"}, status=500)

        except Exception as e:
            return Response({"error": str(e)}, status=500)