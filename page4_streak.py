#!/usr/bin/env python3
"""
Page 4: Longest Streak

Shows the user's longest consecutive day streak of ChatGPT usage,
along with the start and end dates of that streak.
"""
import pickle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440


def create_overlay():
    """Generate the streak information overlay for page 4."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)

    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    yellow = HexColor("#FFD700")

    # Large streak number in the center
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 200)
    days = str(data['longest_streak'])
    c.drawCentredString(PAGE_WIDTH / 2, 1050, days)

    # "DAYS" label below the number
    c.setFont("Helvetica-Bold", 60)
    c.drawCentredString(PAGE_WIDTH / 2, 975, "DAYS")

    # Start date (positioned above the arrow graphic)
    if data['streak_start']:
        start_str = data['streak_start'].strftime('%b %d').upper()
        c.setFillColor(yellow)
        c.setFont("Helvetica-Bold", 50)
        c.drawCentredString(PAGE_WIDTH / 2, 870, start_str)

    # End date (positioned below the arrow graphic)
    if data['streak_end']:
        end_str = data['streak_end'].strftime('%b %d').upper()
        c.setFillColor(yellow)
        c.setFont("Helvetica-Bold", 50)
        c.drawCentredString(PAGE_WIDTH / 2, 650, end_str)

    c.save()
    packet.seek(0)
    return packet


if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print("Page 4 overlay created")
