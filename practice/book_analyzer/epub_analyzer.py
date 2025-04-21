import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import chardet
import numpy as np

# Загружаем необходимые данные NLTK
nltk.download('punkt')

def detect_encoding(content):
    """
    Определяет кодировку содержимого
    """
    result = chardet.detect(content)
    return result['encoding']

def extract_text_from_epub(epub_path):
    """
    Извлекает текст из EPUB файла
    """
    book = epub.read_epub(epub_path)
    text = ""
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Получаем содержимое HTML
            content = item.get_content()
            # Определяем кодировку
            encoding = detect_encoding(content)
            try:
                # Пробуем декодировать с определенной кодировкой
                html_content = content.decode(encoding)
            except UnicodeDecodeError:
                # Если не получилось, пробуем другие распространенные кодировки
                for enc in ['utf-8', 'windows-1251', 'cp1251', 'latin1']:
                    try:
                        html_content = content.decode(enc)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    print(f"Предупреждение: не удалось декодировать часть содержимого")
                    continue
            
            # Используем BeautifulSoup для извлечения текста
            soup = BeautifulSoup(html_content, 'html.parser')
            text += soup.get_text() + "\n"
    
    return text

def get_word_frequency(text, top_n=10):
    """
    Возвращает частоту встречаемости слов
    """
    # Очищаем текст от знаков препинания и приводим к нижнему регистру
    words = re.findall(r'\b\w+\b', text.lower())
    # Исключаем короткие слова (менее 3 букв)
    words = [word for word in words if len(word) > 2]
    return Counter(words).most_common(top_n)

def analyze_word_vectors(text, top_n=5):
    """
    Анализирует векторы слов с помощью TF-IDF
    """
    # Токенизируем текст на предложения
    sentences = sent_tokenize(text)
    
    # Создаем TF-IDF векторизатор
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # Получаем список всех слов
    feature_names = vectorizer.get_feature_names_out()
    
    # Находим наиболее похожие слова для каждого из топ-N частых слов
    print("\nАнализ семантических связей:")
    frequent_words = [word for word, _ in get_word_frequency(text, top_n)]
    
    for word in frequent_words:
        if word in feature_names:
            # Получаем индекс слова
            word_idx = np.where(feature_names == word)[0][0]
            # Получаем TF-IDF значения для этого слова во всех предложениях
            word_scores = tfidf_matrix[:, word_idx].toarray().flatten()
            # Находим предложения с высоким TF-IDF значением для этого слова
            top_sentences = np.argsort(word_scores)[-3:][::-1]
            
            print(f"\nКонтекст для слова '{word}':")
            for idx in top_sentences:
                if word_scores[idx] > 0:
                    print(f"  - {sentences[idx]} (важность: {word_scores[idx]:.2f})")
    
    return vectorizer, tfidf_matrix

def analyze_book(epub_path):
    """
    Анализирует книгу и выводит базовую информацию
    """
    book = epub.read_epub(epub_path)
    
    # Получаем метаданные
    title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else "Неизвестно"
    author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else "Неизвестно"
    
    print(f"Название: {title}")
    print(f"Автор: {author}")
    
    # Извлекаем текст
    text = extract_text_from_epub(epub_path)
    
    # Базовая статистика
    words = text.split()
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    print(f"\nСтатистика:")
    print(f"Количество слов: {len(words)}")
    print(f"Количество предложений: {len(sentences)}")
    print(f"Средняя длина предложения: {len(words)/len(sentences):.2f} слов")
    
    # Выводим первые 5 предложений
    print("\nПервые 5 предложений:")
    for i, sentence in enumerate(sentences[:5], 1):
        print(f"{i}. {sentence}")
    
    # Анализ частоты слов
    print("\nТоп-10 самых частых слов:")
    word_freq = get_word_frequency(text)
    for word, count in word_freq:
        print(f"{word}: {count} раз")
    
    # Анализ векторов слов
    vectorizer, tfidf_matrix = analyze_word_vectors(text)

if __name__ == "__main__":
    epub_path = "book.epub"  # Путь к вашему EPUB файлу
    if os.path.exists(epub_path):
        analyze_book(epub_path)
    else:
        print(f"Файл {epub_path} не найден!") 