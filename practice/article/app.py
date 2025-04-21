from flask import Flask, render_template, jsonify
import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import json
import re

app = Flask(__name__)

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Read the article from file
def read_article():
    try:
        with open('article.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading article: {e}")
        return "Error reading article file."

# Extract keywords and abstract from the article
def extract_metadata(text):
    # Extract abstract
    abstract_match = re.search(r'Abstract:\s*(.*?)(?=\n\n|\nKeywords:)', text, re.DOTALL)
    abstract = abstract_match.group(1).strip() if abstract_match else ""
    
    # Extract keywords
    keywords_match = re.search(r'Keywords:\s*(.*?)(?=\n\n|\nIntroduction:)', text, re.DOTALL)
    keywords_text = keywords_match.group(1).strip() if keywords_match else ""
    keywords = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
    
    # Extract named entities using spaCy
    doc = nlp(text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    
    return {
        'abstract': abstract,
        'keywords': keywords,
        'entities': entities
    }

@app.route('/')
def index():
    article_text = read_article()
    metadata = extract_metadata(article_text)
    return render_template('index.html', 
                          article_text=article_text, 
                          keywords=metadata['keywords'],
                          entities=metadata['entities'],
                          abstract=metadata['abstract'])

if __name__ == '__main__':
    app.run(debug=True, port=5001) 