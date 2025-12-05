#!/usr/bin/env python3
"""
Page 12: Visual summary of the year
Headers: "GPT SUMMARY" at y=52
Content area: y=200-1300
"""
import pickle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440

def create_overlay():
    """Create overlay for page 12 with year summary."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)
    
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # Colors
    dark_bg = HexColor("#0d0d0d")
    orange = HexColor("#FF8C00")
    yellow = HexColor("#FFD700")
    coral = HexColor("#FF6B6B")
    teal = HexColor("#20B2AA")
    purple = HexColor("#9370DB")
    green = HexColor("#32CD32")
    
    # Main background
    c.setFillColor(dark_bg)
    c.roundRect(40, 200, PAGE_WIDTH - 80, 1050, 25, fill=True, stroke=False)
    
    # Summary stats in grid
    stats = [
        ("CONVERSATIONS", f"{data['total_conversations']:,}", orange),
        ("WORDS SENT", f"{data['user_words']:,}", yellow),
        ("WORDS RECEIVED", f"{data['gpt_words']:,}", coral),
        ("MESSAGES SENT", f"{data['user_messages']:,}", teal),
        ("LONGEST STREAK", f"{data['longest_streak']} DAYS", purple),
        ("TOP MODEL", data['model_usage'][0][0].upper(), green),
    ]
    
    # Grid layout: 2 columns, 3 rows
    col_width = (PAGE_WIDTH - 100) / 2
    row_height = 300
    start_y = 950
    
    for i, (label, value, color) in enumerate(stats):
        col = i % 2
        row = i // 2
        
        x = 60 + col * col_width + col_width / 2
        y = start_y - row * row_height
        
        # Card background
        card_width = col_width - 30
        card_height = 260
        c.setFillColor(HexColor("#1a1a1a"))
        c.roundRect(60 + col * col_width + 15, y - card_height + 100, 
                    card_width, card_height, 15, fill=True, stroke=False)
        
        # Accent bar at top
        c.setFillColor(color)
        c.roundRect(60 + col * col_width + 15, y + 95, card_width, 10, 5, fill=True, stroke=False)
        
        # Label
        c.setFillColor(HexColor("#888888"))
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(x, y + 50, label)
        
        # Value
        c.setFillColor(white)
        font_size = 46 if len(value) < 12 else 34
        c.setFont("Helvetica-Bold", font_size)
        c.drawCentredString(x, y - 30, value)
    
    # Bottom highlight - favorite word
    c.setFillColor(orange)
    c.setFont("Helvetica-Bold", 26)
    fav_word = data['top_words'][0][0].upper()
    fav_count = data['top_words'][0][1]
    c.drawCentredString(PAGE_WIDTH / 2, 270, 
                        f'FAVORITE WORD: "{fav_word}" ({fav_count:,} times)')
    
    c.save()
    packet.seek(0)
    return packet

if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print(f"Page 12 overlay created")
