import pytesseract
from PIL import Image
import pandas as pd

def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def text_to_excel(text, excel_path):
    lines = text.split('\n')
    data = [line.split() for line in lines]
    df = pd.DataFrame(data)
    df.to_excel(excel_path)
image_path = input("Please enter the path to your image file: ").strip('\"')

excel_path = input("Please enter the path where you want to save the Excel file: ").strip('\"')

if not (excel_path.endswith('.xlsx') or excel_path.endswith('.xls')):
    print("Error: The Excel file path should end with .xlsx or .xls")
else:import pytesseract
from PIL import Image
import pandas as pd

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def text_to_excel(text, excel_path):
    lines = text.split('\n')
    data = [line.split() for line in lines]
    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False, header=False)  # Adjusted to exclude index and header

image_path = input("Please enter the path to your image file: ").strip('\"')
excel_path = input("Please enter the path where you want to save the Excel file: ").strip('\"')

if not (excel_path.endswith('.xlsx') or excel_path.endswith('.xls')):
    print("Error: The Excel file path should end with .xlsx or .xls")
else:
    text = image_to_text(image_path)
    text_to_excel(text, excel_path)
    print(f"Excel file saved successfully at {excel_path}")

    text = image_to_text(image_path)
    text_to_excel(text, excel_path)