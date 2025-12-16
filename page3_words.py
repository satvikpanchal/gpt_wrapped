#!/usr/bin/env python3
"""
Page 3: Word Counts

Displays the total words sent and received in the two yellow highlight boxes.
The top box shows words the user typed, the bottom shows GPT's responses.
"""
import pickle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440


def create_overlay():
    """Generate the word count overlay for page 3."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)

    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # Dark text color for contrast against the yellow boxes
    text_color = HexColor("#1a1a1a")
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", 90)

    # Words the user sent (top yellow box)
    user_words = f"{data['user_words']:,}"
    c.drawCentredString(PAGE_WIDTH / 2, 855, user_words)

    # Words GPT sent back (bottom yellow box)
    gpt_words = f"{data['gpt_words']:,}"
    c.drawCentredString(PAGE_WIDTH / 2, 400, gpt_words)

    c.save()
    packet.seek(0)
    return packet


if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print("Page 3 overlay created")
