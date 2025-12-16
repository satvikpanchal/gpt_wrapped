#!/usr/bin/env python3
"""
Page 5: Top 10 Words

Displays a ranked list of the user's most frequently used words,
styled as a colorful table with a frosted glass background.
"""
import pickle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440


def create_overlay():
    """Generate the top words table overlay for page 5."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)

    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # Table layout settings
    table_x = 70
    row_height = 70
    table_width = PAGE_WIDTH - 140
    num_items = len(data['top_words'][:10])

    # Center the table vertically on the page
    table_total_height = num_items * row_height
    table_y_start = 725 + (table_total_height / 2)

    # Frosted glass background behind the table
    bg_padding = 25
    bg_y = table_y_start - table_total_height - bg_padding + 12
    bg_height = table_total_height + (bg_padding * 2) - 4

    glass_color = Color(0.95, 0.95, 0.92, alpha=0.75)
    c.setFillColor(glass_color)
    c.roundRect(table_x - bg_padding, bg_y, table_width + (bg_padding * 2), bg_height, 20, fill=True, stroke=False)

    # Subtle white border for depth
    c.setStrokeColor(Color(1, 1, 1, alpha=0.5))
    c.setLineWidth(2)
    c.roundRect(table_x - bg_padding, bg_y, table_width + (bg_padding * 2), bg_height, 20, fill=False, stroke=True)

    # Warm gradient colors for each row (orange to gold)
    row_colors = [
        HexColor("#FF5500"),
        HexColor("#FF6A00"),
        HexColor("#FF7F00"),
        HexColor("#FF9400"),
        HexColor("#FFA900"),
        HexColor("#FFBE00"),
        HexColor("#FFD300"),
        HexColor("#E8C800"),
        HexColor("#D1BD00"),
        HexColor("#BAB200"),
    ]

    dark_text = HexColor("#1a1a1a")

    # Draw each word row
    for i, (word, count) in enumerate(data['top_words'][:10]):
        y_pos = table_y_start - (i * row_height)

        # Colored row background
        c.setFillColor(row_colors[i])
        c.roundRect(table_x, y_pos - row_height + 12, table_width, row_height - 8, 8, fill=True, stroke=False)

        # Rank number on the left
        c.setFillColor(dark_text)
        c.setFont("Helvetica-Bold", 32)
        c.drawString(table_x + 18, y_pos - 42, f"{i+1}.")

        # The word itself
        c.setFont("Helvetica-Bold", 36)
        c.drawString(table_x + 75, y_pos - 42, word.upper())

        # Usage count on the right
        c.setFont("Helvetica-Bold", 32)
        count_str = f"{count:,}"
        c.drawRightString(table_x + table_width - 18, y_pos - 42, count_str)

    c.save()
    packet.seek(0)
    return packet


if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print("Page 5 overlay created")
