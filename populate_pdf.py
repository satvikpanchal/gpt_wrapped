#!/usr/bin/env python3
"""
Populate the GPT Wrapped PDF with actual data from conversations.
"""
import json
from datetime import datetime
from collections import Counter
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, white, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os

# Load data file path from config
def load_config():
    """Read the data file path from config.txt"""
    config_path = os.path.join(os.path.dirname(__file__), "config.txt")
    with open(config_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("DATA_FILE="):
                return line.split("=", 1)[1].strip()
    raise ValueError("DATA_FILE not found in config.txt")

DATA_FILE = load_config()
PDF_FILE = "GPT_WRAPPED_TEMPLATE.pdf"
OUTPUT_FILE = "gpt_wrapped_2025_populated.pdf"
CUTOFF = datetime(2025, 1, 1)

# Page dimensions (from PDF: 810 x 1440 points)
PAGE_WIDTH = 810
PAGE_HEIGHT = 1440

def load_data():
    """Load and filter conversation data."""
    with open(DATA_FILE, "r") as f:
        conversations = json.load(f)
    
    filtered = []
    for c in conversations:
        if c.get("create_time"):
            ct = datetime.fromtimestamp(c["create_time"])
            if ct >= CUTOFF:
                filtered.append(c)
    
    return filtered

def analyze_data(conversations):
    """Extract all analytics from conversations."""
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", 
                  "is", "it", "that", "this", "with", "as", "be", "are", "was", "were", "been", 
                  "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", 
                  "should", "may", "might", "can", "i", "you", "he", "she", "we", "they", "my", 
                  "your", "his", "her", "our", "their", "what", "which", "who", "how", "when", 
                  "where", "why", "if", "then", "else", "not", "no", "yes", "so", "just", "like", 
                  "more", "some", "any", "all", "also", "from", "by", "about", "into", "through", 
                  "during", "before", "after", "above", "below", "between", "under", "over", 
                  "out", "up", "down", "off", "such", "there", "here", "than", "its", "let", "me"}
    
    # Longest chat
    longest_chat = None
    max_messages = 0
    
    # Prompts
    user_prompts = []
    
    # Words
    all_words = []
    
    # Models
    model_counts = Counter()
    
    for c in conversations:
        msg_count = 0
        for node_id, node in c.get("mapping", {}).items():
            msg = node.get("message")
            if msg and msg.get("content", {}).get("parts"):
                text = " ".join(str(p) for p in msg["content"]["parts"] if isinstance(p, str))
                if text.strip():
                    msg_count += 1
                    
                    # Check role
                    role = msg.get("author", {}).get("role")
                    if role == "user":
                        word_count = len(text.split())
                        user_prompts.append((word_count, c.get("title", "Untitled")))
                        
                        # Word frequency
                        words = text.lower().split()
                        for word in words:
                            cleaned = ''.join(ch for ch in word if ch.isalnum())
                            if cleaned and len(cleaned) > 2 and cleaned not in stop_words:
                                all_words.append(cleaned)
                    
                    elif role == "assistant":
                        model = msg.get("metadata", {}).get("model_slug", "unknown")
                        if model:
                            model_counts[model] += 1
        
        if msg_count > max_messages:
            max_messages = msg_count
            longest_chat = c
    
    user_prompts.sort(reverse=True)
    word_freq = Counter(all_words)
    
    return {
        "longest_chat_title": longest_chat.get("title", "Untitled") if longest_chat else "N/A",
        "longest_chat_messages": max_messages,
        "top_prompts": user_prompts[:10],
        "top_words": word_freq.most_common(10),
        "model_usage": model_counts.most_common(6)
    }

def create_overlay(page_num, data, width, height):
    """Create a transparent overlay PDF for a specific page."""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    
    # Colors matching the template
    orange = HexColor("#FF8210")
    yellow = HexColor("#FFC24A")
    white_color = white
    
    if page_num == 5:  # Top 10 Words (page 5, 0-indexed 4)
        # The template has headers, we need to add the word list
        # Starting position based on template analysis
        y_start = height - 250  # Start below the header
        
        c.setFillColor(white_color)
        c.setFont("Helvetica-Bold", 36)
        
        for i, (word, count) in enumerate(data["top_words"]):
            y_pos = y_start - (i * 60)
            # Word on left, count on right
            c.drawString(80, y_pos, f"{i+1}. {word.upper()}")
            c.drawRightString(width - 80, y_pos, f"{count:,}")
    
    elif page_num == 6:  # Model palette (page 6, 0-indexed 5)
        y_start = height - 280
        
        c.setFillColor(white_color)
        total = sum(count for _, count in data["model_usage"])
        
        for i, (model, count) in enumerate(data["model_usage"]):
            y_pos = y_start - (i * 70)
            pct = (count / total) * 100 if total > 0 else 0
            
            c.setFont("Helvetica-Bold", 32)
            c.drawString(80, y_pos, model.upper())
            
            c.setFont("Helvetica", 28)
            c.drawRightString(width - 80, y_pos, f"{pct:.1f}%")
    
    elif page_num == 7:  # Longest chat (page 7, 0-indexed 6)
        # Fill in the XXXXX placeholders - need to cover them with background first
        
        # Draw background rectangles to cover XXXXX placeholders
        # Based on PDF coords: left XXXXX at x=0, y=66, right XXXXX at x=638, y=255
        # PDF height is 1440, so convert: pdf_y = height - screen_y
        
        # Cover left placeholder area (topic)
        bg_color = HexColor("#1a1a1a")  # Dark background matching slide
        c.setFillColor(bg_color)
        c.rect(40, height - 810, 350, 100, fill=True, stroke=False)
        
        # Cover right placeholder area (messages)  
        c.rect(420, height - 810, 350, 100, fill=True, stroke=False)
        
        # Now draw the actual text
        c.setFillColor(white_color)
        
        c.setFont("Helvetica-Bold", 42)
        title = data["longest_chat_title"][:22]  # Truncate if too long
        c.drawString(50, height - 780, title.upper())
        
        # Message count
        c.setFont("Helvetica-Bold", 56)
        c.drawString(480, height - 780, str(data["longest_chat_messages"]))
    
    elif page_num == 10:  # Top 10 Longest Prompts (page 10, 0-indexed 9)
        y_start = height - 280
        
        c.setFillColor(white_color)
        
        for i, (word_count, title) in enumerate(data["top_prompts"]):
            y_pos = y_start - (i * 60)
            
            c.setFont("Helvetica-Bold", 28)
            truncated_title = title[:35] + "..." if len(title) > 35 else title
            c.drawString(80, y_pos, f"{i+1}. {truncated_title}")
            
            c.setFont("Helvetica", 28)
            c.drawRightString(width - 80, y_pos, f"{word_count:,}")
    
    elif page_num == 11:  # GPT Persona (page 11, 0-indexed 10)
        c.setFillColor(white_color)
        c.setFont("Helvetica-Bold", 36)
        
        # Based on the data, create a persona description
        top_topics = [title for _, title in data["top_prompts"][:3]]
        
        y_pos = height - 350
        c.drawString(80, y_pos, "THE DEBUGGER")
        
        c.setFont("Helvetica", 24)
        y_pos -= 60
        c.drawString(80, y_pos, "You spent most of your time in:")
        
        c.setFont("Helvetica-Bold", 28)
        for i, topic in enumerate(top_topics):
            y_pos -= 50
            truncated = topic[:40] + "..." if len(topic) > 40 else topic
            c.drawString(100, y_pos, f"• {truncated}")
    
    elif page_num == 12:  # Summary (page 12, 0-indexed 11)
        c.setFillColor(white_color)
        c.setFont("Helvetica-Bold", 28)
        
        y_pos = height - 350
        
        # Summary stats
        total_convos = len(conversations) if 'conversations' in dir() else 1735
        c.drawString(80, y_pos, f"TOTAL CONVERSATIONS: 1,735")
        
        y_pos -= 50
        c.drawString(80, y_pos, f"LONGEST CHAT: {data['longest_chat_messages']} MESSAGES")
        
        y_pos -= 50
        c.drawString(80, y_pos, f"TOP MODEL: {data['model_usage'][0][0].upper()}")
        
        y_pos -= 50
        c.drawString(80, y_pos, f"FAVORITE WORD: {data['top_words'][0][0].upper()}")
    
    c.save()
    packet.seek(0)
    return PdfReader(packet)

def main():
    print("Loading conversation data...")
    conversations = load_data()
    print(f"Loaded {len(conversations)} conversations from 2025")
    
    print("Analyzing data...")
    data = analyze_data(conversations)
    
    print(f"  Longest chat: {data['longest_chat_title']} ({data['longest_chat_messages']} messages)")
    print(f"  Top word: {data['top_words'][0][0]} ({data['top_words'][0][1]} times)")
    print(f"  Top model: {data['model_usage'][0][0]}")
    
    print("Opening template PDF...")
    reader = PdfReader(PDF_FILE)
    writer = PdfWriter()
    
    # Pages that need overlays (0-indexed)
    overlay_pages = [4, 5, 6, 9, 10, 11]  # Pages 5, 6, 7, 10, 11, 12
    
    for i, page in enumerate(reader.pages):
        page_num = i + 1
        
        if i in overlay_pages:
            print(f"  Adding overlay to page {page_num}...")
            # Get page dimensions
            mediabox = page.mediabox
            width = float(mediabox.width)
            height = float(mediabox.height)
            
            # Create and merge overlay
            overlay = create_overlay(page_num, data, width, height)
            if len(overlay.pages) > 0:
                page.merge_page(overlay.pages[0])
        
        writer.add_page(page)
    
    print(f"Saving to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "wb") as f:
        writer.write(f)
    
    print("Done! PDF populated with your GPT wrapped data.")

if __name__ == "__main__":
    main()
