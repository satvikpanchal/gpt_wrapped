#!/usr/bin/env python3
"""
Page 12: Year Summary Dashboard

A polished summary page showing all key stats at a glance.
Designed with visual hierarchy: primary stats at top, secondary in middle,
achievements below, and a fun "favorite word" takeaway at the bottom.
"""
import pickle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, Color

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440

def create_overlay():
    """Create overlay for page 12 - premium year-in-review design."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)
    
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # Color palette - refined
    orange = HexColor("#FF8C00")
    dark_text = HexColor("#1a1a1a")
    secondary_text = HexColor("#4a4a4a")
    muted_label = HexColor("#888888")
    light_muted = HexColor("#aaaaaa")
    
    # ========================================
    # MAIN CARD - tighter fit around content
    # ========================================
    
    # Card dimensions - aligned to text edges
    card_top = 1240
    card_bottom = 330
    card_height = card_top - card_bottom
    card_margin = 70
    
    # Shadow layer (offset, more transparent)
    shadow = Color(0, 0, 0, alpha=0.08)
    c.setFillColor(shadow)
    c.roundRect(card_margin + 4, card_bottom - 4, PAGE_WIDTH - card_margin * 2, card_height, 28, fill=True, stroke=False)
    
    # Main card - soft white
    card_bg = Color(0.98, 0.98, 0.96, alpha=0.92)
    c.setFillColor(card_bg)
    c.roundRect(card_margin, card_bottom, PAGE_WIDTH - card_margin * 2, card_height, 25, fill=True, stroke=False)
    
    # Layout constants - columns closer to center
    center_x = PAGE_WIDTH / 2
    left_col = 270
    right_col = 540
    
    # ========================================
    # TOP SECTION - Primary Impact Stats
    # Conversations + Words Sent (the headline numbers)
    # ========================================
    
    top_y = 1180
    
    # CONVERSATIONS - left
    c.setFillColor(muted_label)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(left_col, top_y, "CONVERSATIONS")
    
    c.setFillColor(dark_text)
    c.setFont("Helvetica-Bold", 58)
    c.drawCentredString(left_col, top_y - 65, f"{data['total_conversations']:,}")
    
    # WORDS SENT - right
    c.setFillColor(muted_label)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(right_col, top_y, "WORDS SENT")
    
    c.setFillColor(dark_text)
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(right_col, top_y - 63, f"{data['user_words']:,}")
    
    # ========================================
    # MIDDLE SECTION - Secondary Stats
    # Words Received + Messages Sent
    # ========================================
    
    mid_y = 920
    
    # WORDS RECEIVED - left
    c.setFillColor(muted_label)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(left_col, mid_y, "WORDS RECEIVED")
    
    c.setFillColor(secondary_text)
    c.setFont("Helvetica-Bold", 46)
    c.drawCentredString(left_col, mid_y - 60, f"{data['gpt_words']:,}")
    
    # MESSAGES SENT - right
    c.setFillColor(muted_label)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(right_col, mid_y, "MESSAGES SENT")
    
    c.setFillColor(secondary_text)
    c.setFont("Helvetica-Bold", 52)
    c.drawCentredString(right_col, mid_y - 60, f"{data['user_messages']:,}")
    
    # ========================================
    # BOTTOM SECTION - Achievements
    # Longest Streak + Top Model (special treatment)
    # ========================================
    
    achievement_y = 650
    
    # Subtle separator - breathing room before achievements
    c.setStrokeColor(Color(0, 0, 0, alpha=0.06))
    c.setLineWidth(1)
    c.line(100, achievement_y + 120, PAGE_WIDTH - 100, achievement_y + 120)
    
    # LONGEST STREAK - left (achievement style)
    c.setFillColor(muted_label)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(left_col, achievement_y + 75, "LONGEST STREAK")
    
    c.setFillColor(orange)  # Orange for achievement emphasis
    c.setFont("Helvetica-Bold", 52)
    c.drawCentredString(left_col, achievement_y, f"{data['longest_streak']}")
    
    c.setFillColor(secondary_text)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(left_col, achievement_y - 40, "DAYS")
    
    # TOP MODEL - right (achievement style)
    c.setFillColor(muted_label)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(right_col, achievement_y + 75, "TOP MODEL")
    
    c.setFillColor(orange)  # Orange for achievement emphasis
    c.setFont("Helvetica-Bold", 44)
    model_name = data['model_usage'][0][0].upper().replace('GPT-', 'GPT-')
    c.drawCentredString(right_col, achievement_y - 5, model_name)
    
    # ========================================
    # EASTER EGG - Favorite Word
    # Separated, playful, memorable takeaway
    # ========================================
    
    easter_y = 420
    
    # Subtle pill background for the easter egg
    fav_word = data['top_words'][0][0].upper()
    fav_count = data['top_words'][0][1]
    
    # Small label
    c.setFillColor(muted_label)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(center_x, easter_y + 55, "YOUR FAVORITE WORD")
    
    # The word itself - prominent
    c.setFillColor(orange)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(center_x, easter_y, f'"{fav_word}"')
    
    # Count - smaller, parenthetical
    c.setFillColor(muted_label)
    c.setFont("Helvetica", 14)
    c.drawCentredString(center_x, easter_y - 35, f"used {fav_count:,} times")
    
    c.save()
    packet.seek(0)
    return packet

if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print("Page 12 overlay created")
