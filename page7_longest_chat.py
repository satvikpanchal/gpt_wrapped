#!/usr/bin/env python3
"""
Page 7: Fill in longest chat info at exact XXXXX placeholder positions
PDF coords: y from bottom, page is 810x1440
Placeholders: XXXXX at y=131, x=0, size=136
Template has:
- "A SNAPSHOT OF YOUR LONGEST CHAT" at y=69-255
- "TOPIC OF THE CONVERSATION" (left side)
- "TOTAL MESSAGES EXCHANGED" (right side)
"""
import pickle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440

def create_overlay():
    """Create overlay for page 7 with longest chat info."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)
    
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # Background color
    dark_bg = HexColor("#1a1a1a")
    orange = HexColor("#FF8C00")
    
    # The XXXXX placeholders are at y=131, size=136
    # Two sections side by side:
    # Left: TOPIC OF THE CONVERSATION (around x=0-400)
    # Right: TOTAL MESSAGES EXCHANGED (around x=400-810)
    
    # The content should go below the headers, roughly y=400-700 area
    content_y = 550
    
    # Cover placeholder areas and add content
    # Left side - Topic
    c.setFillColor(dark_bg)
    c.rect(40, content_y - 150, 350, 300, fill=True, stroke=False)
    
    # Right side - Messages
    c.rect(420, content_y - 150, 350, 300, fill=True, stroke=False)
    
    # Draw topic title (word-wrapped)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 32)
    
    title = data['longest_chat_title']
    words = title.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(' '.join(current_line)) > 16:
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(' '.join(current_line))
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    
    y_pos = content_y + 80
    for line in lines[:5]:
        c.drawString(60, y_pos, line.upper())
        y_pos -= 45
    
    # Draw message count
    c.setFillColor(orange)
    c.setFont("Helvetica-Bold", 100)
    c.drawCentredString(595, content_y + 30, str(data['longest_chat_messages']))
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(595, content_y - 50, "MESSAGES")
    
    c.save()
    packet.seek(0)
    return packet

if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print(f"Page 7 overlay created")
