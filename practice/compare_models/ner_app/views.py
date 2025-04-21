from django.shortcuts import render
from django.http import JsonResponse
import spacy
from transformers import pipeline
import nltk
from nltk.tag import StanfordNERTagger
import os

# Download required NLTK data
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Initialize NER models
try:
    spacy_en = spacy.load('en_core_web_sm')
except:
    spacy.cli.download('en_core_web_sm')
    spacy_en = spacy.load('en_core_web_sm')

try:
    spacy_ru = spacy.load('ru_core_news_sm')
except:
    spacy.cli.download('ru_core_news_sm')
    spacy_ru = spacy.load('ru_core_news_sm')

# Initialize Hugging Face transformers
ner_pipeline = pipeline('ner', model='dbmdz/bert-large-cased-finetuned-conll03-english')

def home(request):
    return render(request, 'home.html')

def models(request):
    models_info = {
        'spacy': {
            'name': 'SpaCy',
            'description': 'Industrial-strength Natural Language Processing',
            'languages': ['English', 'Russian'],
            'features': ['Fast', 'Accurate', 'Production-ready']
        },
        'transformers': {
            'name': 'Hugging Face Transformers',
            'description': 'State-of-the-art Natural Language Processing',
            'models': ['BERT', 'RoBERTa'],
            'features': ['High accuracy', 'Multiple languages', 'Easy to use']
        },
        'stanford': {
            'name': 'Stanford NER',
            'description': 'Stanford Named Entity Recognizer',
            'features': ['Well-established', 'Research-grade', 'Java-based']
        },
        'nltk': {
            'name': 'NLTK',
            'description': 'Natural Language Toolkit',
            'features': ['Educational', 'Comprehensive', 'Python-based']
        }
    }
    return render(request, 'models.html', {'models': models_info})

def analyze_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        selected_models = request.POST.getlist('models')
        
        results = {}
        
        if 'spacy' in selected_models:
            # SpaCy analysis
            doc_en = spacy_en(text)
            results['spacy'] = {
                'model': 'en_core_web_sm',
                'entities': [{'text': ent.text, 'label': ent.label_} for ent in doc_en.ents]
            }
            
        if 'transformers' in selected_models:
            # Hugging Face transformers analysis
            entities = ner_pipeline(text)
            # Group consecutive tokens with the same label
            grouped_entities = []
            current_entity = None
            
            for ent in entities:
                if current_entity is None:
                    current_entity = {'text': ent['word'], 'label': ent['entity'].replace('-', '')}
                elif ent['entity'].startswith('I-') and ent['entity'][2:] == current_entity['label']:
                    current_entity['text'] += ' ' + ent['word']
                else:
                    grouped_entities.append(current_entity)
                    current_entity = {'text': ent['word'], 'label': ent['entity'].replace('-', '')}
            
            if current_entity:
                grouped_entities.append(current_entity)
            
            results['transformers'] = {
                'model': 'BERT (dbmdz/bert-large-cased-finetuned-conll03-english)',
                'entities': grouped_entities
            }
            
        if 'nltk' in selected_models:
            # NLTK analysis
            tokens = nltk.word_tokenize(text)
            tagged = nltk.pos_tag(tokens)
            entities = nltk.chunk.ne_chunk(tagged)
            nltk_entities = []
            for entity in entities:
                if hasattr(entity, 'label'):
                    nltk_entities.append({
                        'text': ' '.join([child[0] for child in entity]),
                        'label': entity.label()
                    })
            results['nltk'] = {
                'model': 'NLTK NE Chunker',
                'entities': nltk_entities
            }
        
        # Render the results template
        html = render(request, 'analysis_results.html', {'results': results}).content.decode('utf-8')
        return JsonResponse({'html': html})
    
    return JsonResponse({'error': 'Invalid request method'})
