import nltk
import spacy
from collections import Counter
import os

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def analyze_text(file_path):
    # Read the text file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Count words
    words = nltk.word_tokenize(text)
    word_count = len(words)
    
    # Extract named entities using spaCy
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Count entities by type
    entity_counts = Counter([label for _, label in entities])
    
    # Print results
    print(f"\nTotal word count: {word_count}")
    print("\nNamed Entities by type:")
    for entity_type, count in entity_counts.items():
        print(f"{entity_type}: {count}")
    
    print("\nDetailed named entities:")
    for entity, label in entities:
        print(f"{entity} ({label})")

if __name__ == "__main__":
    # Specify the path to your book file
    book_path = "book.txt"  # Change this to your book file path
    analyze_text(book_path) 