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

output_dir = './out/hackathon'
os.makedirs(output_dir, exist_ok=True)

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

csv_path = "hackathon.csv"
template_pdf_path = "./certs/hackathon.pdf"

with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 
    
    for row in reader:
        if len(row) < 5:
            continue
            
        timestamp = row[0]
        team_name = row[1]
        
        teammates = [
            (row[2], row[3]),  # Team Leader (Teammate 1)
            (row[7], row[8]),  # Teammate 2
            (row[9], row[10]),  # Teammate 3
            (row[11], row[12])  # Teammate 4
        ]
        
        for i, (name, roll_no) in enumerate(teammates):
            if not name or name.strip() == '':
                continue
                
            name = name.strip()
            roll_no = roll_no.strip() if roll_no else ''
            
            if roll_no:
                filename = roll_no.lower().replace(' ', '')
                
                output_pdf_path = f"{output_dir}/{filename}.pdf"
                
                add_text_to_pdf(
                    template_pdf_path,
                    output_pdf_path,
                    name,
                    y_pos=290,
                    font_size=30
                )
                
                print(f"Created certificate for {name} - Team: {team_name}")
