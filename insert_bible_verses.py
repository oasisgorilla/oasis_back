import os
import django

"""
이 프로그램 쓰면 중간중간 파싱 안되는 것도 있기 때문에 한 권씩 넣는 코드로 바꿔서 확인해가며 넣어야 한다.
"""

# Django 프로젝트 설정 불러오기
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from bible.models import BibleVerse

def parse_verse_line(line, file_num):
    """텍스트 파일 한 줄을 파싱해서 책, 장, 절, 텍스트 반환"""
    try:
        ref, text = line.split(" ", 1)
        book_chapter, verse = ref.split(":")
        books = ["Genesis",
                 "Exodus",
                 "Leviticus",
                 "Numbers",
                 "Deuteronomy",
                 "Joshua",
                 "Judges",
                 "Ruth",
                 "1 Samuel",
                 "2 Samuel",
                 "1 Kings",
                 "2 Kings",
                 "1 Chronicles",
                 "2 Chronicles",
                 "Ezra",
                 "Nehemiah",
                 "Esther",
                 "Job",
                 "Psalms",
                 "Proverbs",
                 "Ecclesiastes",
                 "Song of Solomon",
                 "Isaiah",
                 "Jeremiah",
                 "Lamentations",
                 "Ezekiel",
                 "Daniel",
                 "Hosea",
                 "Joel",
                 "Amos",
                 "Obadiah",
                 "Jonah",
                 "Micah",
                 "Nahum",
                 "Habakkuk",
                 "Zephaniah",
                 "Haggai",
                 "Zechariah",
                 "Malachi",
                 "Matthew",
                 "Mark",
                 "Luke",
                 "John",
                 "Acts",
                 "Romans",
                 "1 Corinthians",
                 "2 Corinthians",
                 "Galatians",
                 "Ephesians",
                 "Philippians",
                 "Colossians",
                 "1 Thessalonians",
                 "2 Thessalonians",
                 "1 Timothy",
                 "2 Timothy",
                 "Titus",
                 "Philemon",
                 "Hebrews",
                 "James",
                 "1 Peter",
                 "2 Peter",
                 "1 John",
                 "2 John",
                 "3 John",
                 "Jude",
                 "Revelation"]
        
        if book_chapter[1].isdigit(): # 장 번호
            chapter = int(book_chapter[1:])
        else:
            chapter = int(book_chapter[2:])

        book = books[file_num]  # 책 이름 (예: Genesis)

        verse = int(verse)  # 절 번호
        return book, chapter, verse, text.strip()
    except ValueError:
        print(f"Error parsing line: {line}")
        return None

def insert_verses_from_file(filepath, file_num):
    """텍스트 파일의 구절을 데이터베이스에 삽입"""
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                data = parse_verse_line(line, file_num)
                if data:
                    book, chapter, verse, text = data

                    text = text.replace('\x00', '')
                    BibleVerse.objects.create(book=book, chapter=chapter, verse=verse, text=text)
                    print(f"Inserted: {book} {chapter}:{verse}")

if __name__ == "__main__":

    for i in range(66):
        file_names = ["1-01창세기", 
                      "1-02출애굽기", 
                      "1-03레위기", 
                      "1-04민수기", 
                      "1-05신명기", 
                      "1-06여호수아", 
                      "1-07사사기", 
                      "1-08룻기", 
                      "1-09사무엘상", 
                      "1-10사무엘하", 
                      "1-11열왕기상", 
                      "1-12열왕기하", 
                      "1-13역대상", 
                      "1-14역대하", 
                      "1-15에스라", 
                      "1-16느헤미야", 
                      "1-17에스더", 
                      "1-18욥기", 
                      "1-19시편", 
                      "1-20잠언", 
                      "1-21전도서", 
                      "1-22아가", 
                      "1-23이사야", 
                      "1-24예레미야",
                      "1-25예레미야애가",
                      "1-26에스겔",
                      "1-27다니엘",
                      "1-28호세아",
                      "1-29요엘",
                      "1-30아모스",
                      "1-31오바댜",
                      "1-32요나",
                      "1-33미가",
                      "1-34나훔",
                      "1-35하박국",
                      "1-36스바냐",
                      "1-37학개",
                      "1-38스가랴",
                      "1-39말라기",
                      "2-01마태복음",
                      "2-02마가복음",
                      "2-03누가복음",
                      "2-04요한복음",
                      "2-05사도행전",
                      "2-06로마서",
                      "2-07고린도전서",
                      "2-08고린도후서",
                      "2-09갈라디아서",
                      "2-10에베소서",
                      "2-11빌립보서",
                      "2-12골로새서",
                      "2-13데살로니가전서",
                      "2-14데살로니가후서",
                      "2-15디모데전서",
                      "2-16디모데후서",
                      "2-17디도서",
                      "2-18빌레몬서",
                      "2-19히브리서",
                      "2-20야고보서",
                      "2-21베드로전서",
                      "2-22베드로후서",
                      "2-23요한일서",
                      "2-24요한이서",
                      "2-25요한삼서",
                      "2-26유다서",
                      "2-27요한계시록"]
        
        file_path = "./bible_source/"+file_names[i]+".txt"  # 대상 파일 utf-8로 인코딩 후에 경로 설정할 것!!!, 저장 전 book 변수 이름 바꿨나 확인할것!!!
        insert_verses_from_file(file_path, i)