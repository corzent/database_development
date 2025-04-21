import pdfplumber
import csv
import re
from langdetect import detect

# Open the PDF
with pdfplumber.open("./pdffile.pdf") as pdf:
    # Extract text from all pages
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text()

# Function to detect language of the text
def detect_language(text):
    return detect(text)

# Function to extract relevant content
def extract_keywords_abstract(text):
    # Extract title (Theme), abstract and keywords using regex
    theme_pattern = r"(?:Тема|Title):\s*(.*)"
    abstract_pattern = r"(?:Аннотация|Abstract|Keywords)(.*?)(?:Ключевые слова|Keywords)"
    keywords_pattern = r"(?:Ключевые слова|Keywords):\s*(.*)"

    theme = re.search(theme_pattern, text)
    abstract = re.search(abstract_pattern, text, re.DOTALL)
    keywords = re.search(keywords_pattern, text)

    return (theme.group(1) if theme else None, 
            abstract.group(1) if abstract else None,
            keywords.group(1) if keywords else None)

# Split the document into sections and process each one
sections = full_text.split("Заголовок")  # Adjust this based on how sections are separated in your document

data = []
for section in sections:
    theme, abstract, keywords = extract_keywords_abstract(section)
    if theme or abstract or keywords:
        language = detect_language(abstract or theme or keywords)  # Detect language from any text field
        data.append([theme, abstract, keywords, language])

# Save to CSV
with open("articles_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Theme", "Abstract", "Keywords", "Language"])
    writer.writerows(data)

print("Data has been saved to 'articles_data.csv'")
