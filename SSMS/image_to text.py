import pytesseract
from PIL import Image
from docx import Document

pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def image_to_text(image_path):
    # Open the image file
    img = Image.open(image_path)
    
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    
    return text

def save_to_word(text, output_path):
    # Create a new Document
    doc = Document()
    
    # Add the extracted text to the document
    doc.add_paragraph(text)
    
    # Save the document
    doc.save(output_path)

def main():
    image_path = r'C:\Users\Nikhil Sharma\Downloads\pytessaract-test1.png'
    output_docx_path = r'C:\Users\Nikhil Sharma\Downloads\extracted_text.docx'

    extracted_text = image_to_text(image_path)

    # Save extracted text to Word document
    save_to_word(extracted_text, output_docx_path)

    print(f"Text extracted from image and saved to '{output_docx_path}'.")

if __name__ == "__main__":
    main()
