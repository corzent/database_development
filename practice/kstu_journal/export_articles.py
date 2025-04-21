import os
import django
import csv
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_project.settings')
django.setup()

from articles.models import Article

def export_articles_to_csv():
    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'articles_export_{timestamp}.csv'
    
    # Define CSV headers
    headers = [
        'Article ID',
        'Annotation (Kyrgyz)',
        'Annotation (Russian)',
        'Annotation (English)',
        'Keywords (Kyrgyz)',
        'Keywords (Russian)',
        'Keywords (English)',
        'Created At'
    ]
    
    # Get all articles
    articles = Article.objects.all()
    
    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        for article in articles:
            row = [
                article.id,
                article.annotation_ky,
                article.annotation_ru,
                article.annotation_en,
                article.keywords_ky,
                article.keywords_ru,
                article.keywords_en,
                article.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ]
            writer.writerow(row)
    
    print(f'Articles exported to {filename}')

if __name__ == '__main__':
    export_articles_to_csv() 