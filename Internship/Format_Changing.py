import pytesseract
from PIL import Image
from openpyxl import Workbook
from openpyxl.styles import Alignment

image_path = r'C:\Users\Nikhil Sharma\Pictures\Screenshots\Screenshot 2024-07-01 112413.png'

text = pytesseract.image_to_string(Image.open(image_path))
wb = Workbook()
ws = wb.active
ws.title = 'OCR Data'

lines = text.splitlines()

for r, line in enumerate(lines, start=1):
    cell = ws.cell(row=r, column=1, value=line)
    cell.alignment = Alignment(wrap_text=True)  

excel_file = r'C:\Users\Nikhil Sharma\Desktop\Internship\new.xlsx'
wb.save(excel_file)

print(f'OCR data has been written to {excel_file}')
