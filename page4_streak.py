#!/usr/bin/env python3
"""
Page 4: Streak info
Based on coordinate reference:
- Streak number (large): around y=1050, centered
- "DAYS" unit: around y=950
- Start date: above arrow, around y=750
- Arrow already exists at y=800
- End date: below arrow, around y=650
"""
import pickle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440

def create_overlay():
    """Create overlay for page 4 with streak info."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)
    
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # Colors
    yellow = HexColor("#FFD700")
    
    # 1. Streak number (large) - center of blue area
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 200)
    days = str(data['longest_streak'])
    c.drawCentredString(PAGE_WIDTH / 2, 1050, days)
    
    # 2. "DAYS" unit - moved up more to make room
    c.setFont("Helvetica-Bold", 60)
    c.drawCentredString(PAGE_WIDTH / 2, 975, "DAYS")
    
    # 3. Start date - ABOVE the arrow (arrow is at ~y=780)
    if data['streak_start']:
        start_str = data['streak_start'].strftime('%b %d').upper()
        c.setFillColor(yellow)
        c.setFont("Helvetica-Bold", 50)
        c.drawCentredString(PAGE_WIDTH / 2, 890, start_str)
    
    # 4. End date - BELOW the arrow
    if data['streak_end']:
        end_str = data['streak_end'].strftime('%b %d').upper()
        c.setFillColor(yellow)
        c.setFont("Helvetica-Bold", 50)
        c.drawCentredString(PAGE_WIDTH / 2, 730, end_str)
    
    c.save()
    packet.seek(0)
    return packet

if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print(f"Page 4 overlay created")
