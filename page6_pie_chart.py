#!/usr/bin/env python3
"""
Page 6: Pie chart with white opaque square background
"""
import pickle
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from PIL import Image

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440

def create_pie_chart():
    """Create pie chart with vibrant colors."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)
    
    models = []
    counts = []
    for model, count in data['model_usage'][:6]:
        model_name = model.replace("-", " ").upper()
        models.append(model_name)
        counts.append(count)
    
    # Vibrant, distinct colors
    colors = [
        "#E74C3C",  # Red
        "#F39C12",  # Orange
        "#27AE60",  # Green
        "#3498DB",  # Blue
        "#9B59B6",  # Purple
        "#1ABC9C",  # Teal
    ]
    
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="none")
    ax.set_facecolor("none")

    wedges, texts, autotexts = ax.pie(
        counts,
        labels=None,
        autopct=lambda p: f"{p:.1f}%" if p > 2 else "",
        startangle=90,
        colors=colors[:len(counts)],
        wedgeprops=dict(edgecolor="white", linewidth=2),
        pctdistance=0.7
    )

    for t in autotexts:
        t.set_color("white")
        t.set_fontsize(16)
        t.set_fontweight("bold")

    ax.set_aspect("equal")

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=120, transparent=True, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return buf, models, counts

def create_overlay():
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # Generate pie chart
    chart_buf, models, counts = create_pie_chart()
    img = Image.open(chart_buf)

    # Dimensions - wider
    chart_size = 420
    legend_height = 200
    padding = 60
    
    # Total box dimensions - wider
    box_width = chart_size + padding * 3
    box_height = chart_size + legend_height + padding * 2
    
    # Center the box
    box_x = (PAGE_WIDTH - box_width) / 2
    box_y = (PAGE_HEIGHT - box_height) / 2
    
    # Liquid glass / frosted glass effect - semi-transparent with slight tint
    glass_color = Color(0.95, 0.95, 0.92, alpha=0.75)  # Slight warm tint, 75% opacity
    c.setFillColor(glass_color)
    c.roundRect(box_x, box_y, box_width, box_height, 25, fill=True, stroke=False)
    
    # Subtle border for glass effect
    c.setStrokeColor(Color(1, 1, 1, alpha=0.5))
    c.setLineWidth(2)
    c.roundRect(box_x, box_y, box_width, box_height, 25, fill=False, stroke=True)
    
    # Draw pie chart (centered inside the box, upper portion)
    chart_x = box_x + (box_width - chart_size) / 2
    chart_y = box_y + legend_height + padding
    
    img_reader = ImageReader(img)
    c.drawImage(img_reader, chart_x, chart_y, width=chart_size, height=chart_size, mask="auto")

    # Legend (centered inside the box, lower portion)
    colors_hex = ["#E74C3C", "#F39C12", "#27AE60", "#3498DB", "#9B59B6", "#1ABC9C"]
    total = sum(counts)
    
    legend_start_y = box_y + legend_height - 20
    legend_x = box_x + (box_width - 420) / 2  # Center the legend

    c.setFont("Helvetica-Bold", 16)

    for i, (model, count) in enumerate(zip(models, counts)):
        pct = (count / total) * 100
        
        col = i % 2
        row = i // 2
        
        x = legend_x + col * 200
        y = legend_start_y - row * 35
        
        # Color dot
        c.setFillColor(HexColor(colors_hex[i]))
        c.circle(x, y + 5, 8, fill=True, stroke=False)
        
        # Model name
        c.setFillColor(HexColor("#333333"))
        c.drawString(x + 18, y, f"{model} ({pct:.1f}%)")

    c.save()
    packet.seek(0)
    return packet

if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    PdfReader(overlay)
    print("Page 6 overlay created")
