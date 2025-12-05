#!/usr/bin/env python3
"""
Page 10: Top 10 longest prompts - matching page 5 style
"""
import pickle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440

def create_overlay():
    """Create overlay for page 10 with prompts table."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)
    
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # Table settings - matching page 5
    table_x = 70
    row_height = 70
    table_width = PAGE_WIDTH - 140
    num_items = len(data['top_prompts'][:10])
    
    # Calculate centered position
    table_total_height = num_items * row_height
    table_y_start = 725 + (table_total_height / 2)
    
    # Liquid glass background
    bg_padding = 25
    bg_y = table_y_start - table_total_height - bg_padding + 12
    bg_height = table_total_height + (bg_padding * 2) - 4
    
    glass_color = Color(0.95, 0.95, 0.92, alpha=0.75)
    c.setFillColor(glass_color)
    c.roundRect(table_x - bg_padding, bg_y, table_width + (bg_padding * 2), bg_height, 20, fill=True, stroke=False)
    
    # Subtle border
    c.setStrokeColor(Color(1, 1, 1, alpha=0.5))
    c.setLineWidth(2)
    c.roundRect(table_x - bg_padding, bg_y, table_width + (bg_padding * 2), bg_height, 20, fill=False, stroke=True)
    
    # Warm gradient colors (matching page 5 exactly)
    colors = [
        HexColor("#FF5500"),  # 1
        HexColor("#FF6A00"),  # 2
        HexColor("#FF7F00"),  # 3
        HexColor("#FF9400"),  # 4
        HexColor("#FFA900"),  # 5
        HexColor("#FFBE00"),  # 6
        HexColor("#FFD300"),  # 7
        HexColor("#E8C800"),  # 8
        HexColor("#D1BD00"),  # 9
        HexColor("#BAB200"),  # 10
    ]
    
    dark_text = HexColor("#1a1a1a")
    
    for i, (word_count, title) in enumerate(data['top_prompts'][:10]):
        y_pos = table_y_start - (i * row_height)
        
        # Row background
        c.setFillColor(colors[i])
        c.roundRect(table_x, y_pos - row_height + 12, table_width, row_height - 8, 
                    8, fill=True, stroke=False)
        
        # Rank number - matching page 5 font size
        c.setFillColor(dark_text)
        c.setFont("Helvetica-Bold", 32)
        c.drawString(table_x + 18, y_pos - 42, f"{i+1}.")
        
        # Topic title (truncated, UPPERCASE to match page 5)
        truncated_title = title[:20] + "..." if len(title) > 20 else title
        c.setFont("Helvetica-Bold", 32)
        c.drawString(table_x + 75, y_pos - 42, truncated_title.upper())
        
        # Word count (right aligned) - matching page 5 font size
        c.setFont("Helvetica-Bold", 32)
        count_str = f"{word_count:,}"
        c.drawRightString(table_x + table_width - 18, y_pos - 42, count_str)
    
    c.save()
    packet.seek(0)
    return packet

if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print(f"Page 10 overlay created")
