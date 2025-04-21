import PyPDF2
import os

def convert_pdf_to_text(pdf_path, output_path):
    # Open the PDF file in binary mode
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Get the number of pages
        num_pages = len(pdf_reader.pages)
        
        # Open the output file in write mode
        with open(output_path, 'w', encoding='utf-8') as output_file:
            # Extract text from each page
            for page_num in range(num_pages):
                # Get the page object
                page = pdf_reader.pages[page_num]
                
                # Extract text from the page
                text = page.extract_text()
                
                # Write the text to the output file
                output_file.write(f"--- Page {page_num + 1} ---\n")
                output_file.write(text)
                output_file.write('\n\n')

if __name__ == "__main__":
    pdf_path = "pdffile.pdf"
    output_path = "text.txt"
    
    if os.path.exists(pdf_path):
        convert_pdf_to_text(pdf_path, output_path)
        print(f"PDF successfully converted to text. Output saved to {output_path}")
    else:
        print(f"Error: {pdf_path} not found") 