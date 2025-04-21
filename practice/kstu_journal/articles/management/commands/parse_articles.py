from django.core.management.base import BaseCommand
from articles.models import Article
import re

class Command(BaseCommand):
    help = 'Parse articles from a text file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Path to the text file')

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        # Split content into pages
        pages = content.split('--- Page')
        # Skip the first page (usually cover)
        pages = pages[1:]

        current_article = None
        current_section = None
        current_language = None

        for page in pages:
            lines = page.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Check for article title patterns in different languages
                if re.match(r'^[А-Яа-я\s«»]+$', line) and len(line) > 10:
                    if current_article is None:
                        current_article = {
                            'title_ky': line,
                            'title_ru': '',
                            'title_en': '',
                            'annotation_ky': '',
                            'annotation_ru': '',
                            'annotation_en': '',
                            'keywords_ky': '',
                            'keywords_ru': '',
                            'keywords_en': ''
                        }
                        current_language = 'ky'
                    elif current_language == 'ky' and not current_article['title_ru']:
                        current_article['title_ru'] = line
                        current_language = 'ru'
                    elif current_language == 'ru' and not current_article['title_en']:
                        current_article['title_en'] = line
                        current_language = 'en'
                    continue

                # Check for annotation section
                if 'Аннотация' in line or 'Annotation' in line:
                    current_section = 'annotation'
                    continue

                # Check for keywords section
                if 'Ключевые слова' in line or 'Key words' in line or 'Түйүндүү сөздөр' in line:
                    current_section = 'keywords'
                    continue

                # Process content based on current section and language
                if current_section == 'annotation':
                    if re.match(r'^[А-Яа-я\s«»]+$', line):
                        current_article['annotation_ky'] += line + ' '
                    elif re.match(r'^[A-Za-z\s«»]+$', line):
                        current_article['annotation_en'] += line + ' '
                    else:
                        current_article['annotation_ru'] += line + ' '

                elif current_section == 'keywords':
                    if re.match(r'^[А-Яа-я\s«»]+$', line):
                        current_article['keywords_ky'] += line + ' '
                    elif re.match(r'^[A-Za-z\s«»]+$', line):
                        current_article['keywords_en'] += line + ' '
                    else:
                        current_article['keywords_ru'] += line + ' '

                # Check for end of article (new page or new article)
                if line.startswith('--- Page') or (re.match(r'^[А-Яа-я\s«»]+$', line) and len(line) > 10):
                    if current_article and current_article['title_ky'] and current_article['title_ru'] and current_article['title_en']:
                        Article.objects.create(
                            title_ky=current_article['title_ky'].strip(),
                            title_ru=current_article['title_ru'].strip(),
                            title_en=current_article['title_en'].strip(),
                            annotation_ky=current_article['annotation_ky'].strip(),
                            annotation_ru=current_article['annotation_ru'].strip(),
                            annotation_en=current_article['annotation_en'].strip(),
                            keywords_ky=current_article['keywords_ky'].strip(),
                            keywords_ru=current_article['keywords_ru'].strip(),
                            keywords_en=current_article['keywords_en'].strip()
                        )
                    current_article = None
                    current_section = None
                    current_language = None

        # Save the last article if exists
        if current_article and current_article['title_ky'] and current_article['title_ru'] and current_article['title_en']:
            Article.objects.create(
                title_ky=current_article['title_ky'].strip(),
                title_ru=current_article['title_ru'].strip(),
                title_en=current_article['title_en'].strip(),
                annotation_ky=current_article['annotation_ky'].strip(),
                annotation_ru=current_article['annotation_ru'].strip(),
                annotation_en=current_article['annotation_en'].strip(),
                keywords_ky=current_article['keywords_ky'].strip(),
                keywords_ru=current_article['keywords_ru'].strip(),
                keywords_en=current_article['keywords_en'].strip()
            )

        self.stdout.write(self.style.SUCCESS('Successfully parsed articles')) 