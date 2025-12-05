#!/usr/bin/env python3
"""
Page 3: Fill in word counts inside the yellow boxes
Based on coordinate reference:
- Top yellow box (YOU→GPT): y=800-950, center at y=870
- Bottom yellow box (GPT→YOU): y=380-530, center at y=450
"""
import pickle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440

def create_overlay():
    """Create overlay for page 3 with word counts in the yellow boxes."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)
    
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # Text color - dark/black to contrast with yellow background
    text_color = HexColor("#1a1a1a")
    
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", 90)
    
    # YOU → GPT words (top yellow box)
    # Center of box is around y=870, x=center
    user_words = f"{data['user_words']:,}"
    c.drawCentredString(PAGE_WIDTH / 2, 855, user_words)
    
    # GPT → YOU words (bottom yellow box)
    # Moved down a bit from y=435 to y=400
    gpt_words = f"{data['gpt_words']:,}"
    c.drawCentredString(PAGE_WIDTH / 2, 400, gpt_words)
    
    c.save()
    packet.seek(0)
    return packet

if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print(f"Page 3 overlay created")
