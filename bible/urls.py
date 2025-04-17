from django.urls import path
from .views import BibleChapterView

urlpatterns = [
    path('api/bible/<str:book>/<int:chapter>/', BibleChapterView.as_view(), name='bible_chapter'),
    path('api/bible/<str:book>/<int:chapter>/<int:start_verse>/<int:end_verse>/', BibleChapterView.as_view(), name='bible_verse'),
    path('api/chat/', BibleChapterView.as_view(), name='llama_chat'),
]