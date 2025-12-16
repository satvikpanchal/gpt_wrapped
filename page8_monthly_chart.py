#!/usr/bin/env python3
"""
Page 8: Monthly Activity Chart

Shows a horizontal bar chart of conversations per month,
helping visualize usage patterns throughout the year.
"""
import pickle
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from PIL import Image

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440

def create_bar_chart():
    """Create horizontal bar chart with transparent background."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)
    
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 
              'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    counts = [data['monthly_activity'].get(i+1, 0) for i in range(12)]
    
    # Gradient colors based on values
    max_count = max(counts) if max(counts) > 0 else 1
    colors = []
    for count in counts:
        intensity = count / max_count
        r = 1.0
        g = 0.85 - (0.55 * intensity)
        b = 0.15 - (0.15 * intensity)
        colors.append((r, max(0, g), max(0, b)))
    
    # Create figure with transparent background - taller for more space
    fig, ax = plt.subplots(figsize=(10, 14), facecolor='none')
    ax.set_facecolor('none')
    
    y_pos = np.arange(len(months))
    
    # Create horizontal bars
    bars = ax.barh(y_pos, counts, color=colors, height=0.7, 
                   edgecolor='white', linewidth=1)
    
    # Add value labels
    for bar, count in zip(bars, counts):
        width = bar.get_width()
        if width > 0:
            ax.text(width + max(counts)*0.02, bar.get_y() + bar.get_height()/2,
                    f'{count:,}',
                    va='center', ha='left',
                    color='#333333', fontsize=14, fontweight='bold')
    
    # Customize axes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(months, color='#333333', fontsize=16, fontweight='bold')
    ax.invert_yaxis()
    
    # Remove x-axis label (CONVERSATIONS)
    ax.tick_params(axis='x', colors='#333333', labelsize=12)
    
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    ax.set_xlim(0, max(counts) * 1.25 if max(counts) > 0 else 10)
    ax.grid(axis='x', linestyle='--', alpha=0.3, color='#666666')
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', 
                facecolor='none', edgecolor='none', transparent=True)
    plt.close()
    buf.seek(0)
    
    return buf

def create_overlay():
    """Create overlay for page 8 with bar chart."""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # Create bar chart
    chart_buf = create_bar_chart()
    img = Image.open(chart_buf)
    
    # Chart dimensions - taller chart, bottom aligned with "NUMBER OF CONVERSATIONS"
    chart_width = 680
    chart_height = 1020
    chart_x = (PAGE_WIDTH - chart_width) / 2
    chart_y = 200  # Lower to align bottom with text
    
    # Liquid glass background
    padding = 30
    glass_color = Color(0.95, 0.95, 0.92, alpha=0.75)
    c.setFillColor(glass_color)
    c.roundRect(chart_x - padding, chart_y - padding, 
                chart_width + padding * 2, chart_height + padding * 2, 
                20, fill=True, stroke=False)
    
    # Subtle border
    c.setStrokeColor(Color(1, 1, 1, alpha=0.5))
    c.setLineWidth(2)
    c.roundRect(chart_x - padding, chart_y - padding, 
                chart_width + padding * 2, chart_height + padding * 2, 
                20, fill=False, stroke=True)
    
    # Draw the chart image
    img_reader = ImageReader(img)
    c.drawImage(img_reader, chart_x, chart_y, width=chart_width, height=chart_height, 
                mask='auto')
    
    c.save()
    packet.seek(0)
    return packet

if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print("Page 8 overlay created")
