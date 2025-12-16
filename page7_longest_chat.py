#!/usr/bin/env python3
"""
Page 7: Longest Conversation

Displays information about the user's longest conversation,
including the topic title and total message count.
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
    
    # Colors
    orange = HexColor("#FF8C00")
    soft_bg = HexColor("#d8ead8")  # White-greenish background
    
    # =====================================================
    # TOPIC PILL - positioned at y ≈ 870 center
    # =====================================================
    
    # Prepare topic text lines
    title = data['longest_chat_title']
    words = title.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(' '.join(current_line)) > 18:  # Shorter lines for larger font
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(' '.join(current_line))
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    
    # Font and dimensions - similar visual weight to 556 pill
    topic_font_size = 36  # Larger font for better visual balance
    topic_line_height = 44  # Line spacing
    num_lines = min(len(lines), 3)
    topic_cap_height = topic_font_size * 0.72
    
    # Pill center coordinates - moved down for better spacing below "TOPIC OF THE CONVERSATION"
    topic_pill_center_x = PAGE_WIDTH / 2
    topic_pill_center_y = 800
    
    # Find widest line for background
    c.setFont("Helvetica-Bold", topic_font_size)
    max_width = 0
    for line in lines[:num_lines]:
        text_width = c.stringWidth(line.upper(), "Helvetica-Bold", topic_font_size)
        if text_width > max_width:
            max_width = text_width
    
    # Padding - same as 556 pill
    topic_padding_x = 40
    topic_padding_y = 25
    
    # Calculate total text block height
    total_text_height = topic_cap_height + (num_lines - 1) * topic_line_height
    
    # Background dimensions
    topic_bg_width = max_width + topic_padding_x * 2
    topic_bg_height = total_text_height + topic_padding_y * 2
    
    # Position background centered on pill_center
    topic_bg_x = topic_pill_center_x - topic_bg_width / 2
    topic_bg_y = topic_pill_center_y - topic_bg_height / 2
    
    c.setFillColor(soft_bg)
    c.roundRect(topic_bg_x, topic_bg_y, topic_bg_width, topic_bg_height, radius=20, fill=True, stroke=False)
    
    # Draw topic text - optically centered within pill
    # Start from top line, centered vertically
    c.setFillColor(orange)
    c.setFont("Helvetica-Bold", topic_font_size)
    
    # First line baseline: pill_center + half of total text height - cap_height + optical nudge
    optical_nudge = 3
    first_line_baseline = topic_pill_center_y + (total_text_height / 2) - topic_cap_height + optical_nudge
    
    y_pos = first_line_baseline
    for line in lines[:num_lines]:
        c.drawCentredString(topic_pill_center_x, y_pos, line.upper())
        y_pos -= topic_line_height
    
    # =====================================================
    # MESSAGE COUNT PILL - positioned at y ≈ 360 center
    # =====================================================
    msg_text = str(data['longest_chat_messages'])
    msg_font_size = 80  # Sized for visual balance with topic pill
    
    # Pill center coordinates (horizontally centered, vertically at y=360)
    pill_center_x = PAGE_WIDTH / 2  # x = 405
    pill_center_y = 360
    
    # Calculate text dimensions
    c.setFont("Helvetica-Bold", msg_font_size)
    msg_text_width = c.stringWidth(msg_text, "Helvetica-Bold", msg_font_size)
    msg_cap_height = msg_font_size * 0.72  # Cap height for Helvetica Bold
    
    # Use same padding as topic pill for visual consistency
    msg_padding_x = 40
    msg_padding_y = 25
    
    # Background rectangle dimensions
    msg_bg_width = msg_text_width + msg_padding_x * 2
    msg_bg_height = msg_cap_height + msg_padding_y * 2
    
    # Position background centered on pill_center
    msg_bg_x = pill_center_x - msg_bg_width / 2
    msg_bg_y = pill_center_y - msg_bg_height / 2
    
    # Draw rounded background
    c.setFillColor(soft_bg)
    c.roundRect(msg_bg_x, msg_bg_y, msg_bg_width, msg_bg_height, radius=20, fill=True, stroke=False)
    
    # Draw text - optically centered within pill
    # For optical centering: visual center of caps should align with pill center
    # Visual center of text = baseline + cap_height/2
    # So: baseline = pill_center_y - cap_height/2
    # Add small optical adjustment for numeric glyphs
    optical_nudge = 3  # Slight upward for better perceived centering
    text_baseline_y = pill_center_y - msg_cap_height / 2 + optical_nudge
    
    c.setFillColor(orange)
    c.setFont("Helvetica-Bold", msg_font_size)
    c.drawCentredString(pill_center_x, text_baseline_y, msg_text)
    
    c.save()
    packet.seek(0)
    return packet

if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print("Page 7 overlay created")
