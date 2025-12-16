#!/usr/bin/env python3
"""
Page 9: Hourly Activity Heatmap

Breaks down the user's activity across 24 hours, grouped into four
time blocks (Night, Morning, Afternoon, Evening) to show when they
chat with GPT the most.
"""
import pickle
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
from PIL import Image

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440

def create_heatmap():
    """Create 4-row time block visualization."""
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)
    
    hourly = [data['hourly_activity'].get(i, 0) for i in range(24)]
    max_activity = max(hourly) if max(hourly) > 0 else 1
    
    # Time blocks with explicit hour ranges
    blocks = [
        ("NIGHT", list(range(0, 6)), hourly[0:6], 
         ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00']),
        ("MORNING", list(range(6, 12)), hourly[6:12],
         ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00']),
        ("AFTERNOON", list(range(12, 18)), hourly[12:18],
         ['12:00', '13:00', '14:00', '15:00', '16:00', '17:00']),
        ("EVENING", list(range(18, 24)), hourly[18:24],
         ['18:00', '19:00', '20:00', '21:00', '22:00', '23:00']),
    ]
    
    # Create figure with 4 subplots - taller
    fig, axes = plt.subplots(4, 1, figsize=(11, 16), facecolor='none')
    fig.subplots_adjust(hspace=0.4)
    
    # Colors for each block
    block_colors = ['#5DADE2', '#F5B041', '#EC7063', '#AF7AC5']
    
    for idx, (ax, (label, hours, values, time_labels)) in enumerate(zip(axes, blocks)):
        ax.set_facecolor('none')
        
        # Create bars
        x = np.arange(len(hours))
        bars = ax.bar(x, values, color=block_colors[idx], edgecolor='white', 
                     linewidth=2, width=0.7, alpha=0.9)
        
        # Add value labels on bars - bolder
        for bar, val in zip(bars, values):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_activity*0.02,
                       f'{int(val)}', ha='center', va='bottom', fontsize=14, 
                       fontweight='black', color='#1a1a1a')
        
        # Explicit time labels at bottom - bolder
        ax.set_xticks(x)
        ax.set_xticklabels(time_labels, fontsize=13, fontweight='black', color='#1a1a1a')
        
        # Block label on top left - bolder
        ax.text(-0.5, max_activity * 1.1, label, fontsize=16, fontweight='black', 
               color=block_colors[idx], ha='left', va='bottom')
        
        # Style
        ax.set_ylim(0, max_activity * 1.25)
        ax.set_xlim(-0.6, 5.6)
        ax.tick_params(axis='y', colors='#1a1a1a', labelsize=11)
        ax.set_ylabel('Conversations', fontsize=11, fontweight='bold', color='#333333')
        
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        for spine in ['bottom', 'left']:
            ax.spines[spine].set_color('#cccccc')
            ax.spines[spine].set_linewidth(1.5)
        
        ax.grid(axis='y', linestyle='--', alpha=0.3, color='#999999')
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=90, bbox_inches='tight', 
                facecolor='none', edgecolor='none', transparent=True)
    plt.close()
    buf.seek(0)
    
    return buf

def create_overlay():
    """Create overlay for page 9."""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # Create heatmap
    chart_buf = create_heatmap()
    img = Image.open(chart_buf)
    
    # Chart dimensions - taller, moved down
    chart_width = 700
    chart_height = 1000
    chart_x = (PAGE_WIDTH - chart_width) / 2
    chart_y = 180
    
    # Liquid glass background
    padding = 25
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
    
    # Draw the chart
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
    print("Page 9 overlay created")
