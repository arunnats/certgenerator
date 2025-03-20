import csv
import os
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

pdfmetrics.registerFont(TTFont('Poppins', 'Poppins-Regular.ttf'))

output_dirs = {
    'Git': './out/git',
    'Frontend': './out/frontend',
    'Backend': './out/backend',
    'LLMs/RAG': './out/llm'
}

for dir_path in output_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

def add_text_to_pdf(input_pdf_path, output_pdf_path, text, y_pos=400, font_size=24):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    page = reader.pages[0]
    page_width = float(page.mediabox.width)
    
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, float(page.mediabox.height)))
    can.setFont("Poppins", font_size)
    
    text_width = can.stringWidth(text, "Poppins", font_size)
    x_pos = (page_width - text_width) / 2
    
    can.drawString(x_pos, y_pos, text)
    can.save()
    
    packet.seek(0)
    overlay = PdfReader(packet)
    
    page.merge_page(overlay.pages[0])
    writer.add_page(page)
    
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)


csv_path = "workshop.csv"

with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 
    
    for row in reader:
        timestamp, email, name, roll_no, workshops, payment_screenshot = row
        
        username = email.split('@')[0]
        
        workshop_list = workshops.split(', ')
        for workshop in workshop_list:
            if workshop in output_dirs:
                template_pdf_path = f"./certs/{workshop.lower().replace('/', '_')}.pdf"
                output_pdf_path = f"{output_dirs[workshop]}/{username}.pdf"
                
                add_text_to_pdf(
                    template_pdf_path,
                    output_pdf_path,
                    name.strip(),
                    y_pos=312,
                    font_size=30
                )
                
                print(f"Created certificate for {name} - {workshop}")
