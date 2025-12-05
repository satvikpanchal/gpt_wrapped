#!/usr/bin/env python3
"""
Page 11: GPT Persona - bigger image, liquid glass theme
"""
import pickle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from PIL import Image
import os

PAGE_WIDTH = 810
PAGE_HEIGHT = 1440
PERSONA_DIR = "gpt_persona"

PERSONAS = {
    "problemsolver": {
        "keywords": ["error", "fix", "debug", "issue", "problem", "solve", "bug", "crash", "failed", "mismatch", "response"],
        "title": "THE PROBLEM SOLVER",
        "desc": "You dive deep into issues and never give up until the bug is squashed!"
    },
    "builder": {
        "keywords": ["create", "build", "make", "implement", "develop", "app", "website", "project", "code"],
        "title": "THE BUILDER",
        "desc": "You're always creating something new and bringing ideas to life!"
    },
    "researcher": {
        "keywords": ["research", "study", "paper", "analysis", "data", "dataset", "ml", "model", "neural"],
        "title": "THE RESEARCHER", 
        "desc": "You dig deep into knowledge and push the boundaries of understanding!"
    },
    "student": {
        "keywords": ["learn", "homework", "assignment", "class", "course", "exam", "study", "university", "college"],
        "title": "THE SCHOLAR",
        "desc": "You're on a quest for knowledge and crushing those assignments!"
    },
    "explorer": {
        "keywords": ["try", "test", "experiment", "explore", "check", "wonder", "curious"],
        "title": "THE EXPLORER",
        "desc": "You're curious about everything and love to experiment!"
    },
    "organizer": {
        "keywords": ["organize", "plan", "schedule", "list", "todo", "manage", "structure"],
        "title": "THE ORGANIZER",
        "desc": "You keep everything in order and run a tight ship!"
    },
    "strategist": {
        "keywords": ["strategy", "plan", "business", "startup", "growth", "market", "scale"],
        "title": "THE STRATEGIST",
        "desc": "You think big picture and plan for world domination!"
    },
    "brainstormer": {
        "keywords": ["idea", "brainstorm", "creative", "think", "suggest", "help", "advice"],
        "title": "THE BRAINSTORMER",
        "desc": "Your mind is a fountain of ideas and creative solutions!"
    },
    "storyteller": {
        "keywords": ["write", "story", "content", "blog", "article", "text", "email"],
        "title": "THE STORYTELLER",
        "desc": "You craft words into magic and tell compelling stories!"
    },
    "thinker": {
        "keywords": ["understand", "explain", "why", "how", "what", "concept", "theory"],
        "title": "THE DEEP THINKER",
        "desc": "You ponder the big questions and seek deeper understanding!"
    }
}

def select_persona(data):
    all_text = ' '.join([word for word, _ in data['top_words']])
    all_text += ' '.join([title for _, title in data['top_prompts']])
    all_text = all_text.lower()
    
    scores = {}
    for persona, info in PERSONAS.items():
        score = sum(1 for kw in info['keywords'] if kw in all_text)
        scores[persona] = score
    
    best_persona = max(scores, key=scores.get)
    
    if scores[best_persona] == 0:
        if 'response' in all_text or 'error' in all_text or 'mismatch' in all_text:
            best_persona = 'problemsolver'
        else:
            best_persona = 'builder'
    
    return best_persona

def create_overlay():
    with open("extracted_data.pkl", "rb") as f:
        data = pickle.load(f)
    
    persona_key = select_persona(data)
    persona = PERSONAS[persona_key]
    
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # Liquid glass background - moved down
    glass_color = Color(0.95, 0.95, 0.92, alpha=0.75)
    c.setFillColor(glass_color)
    c.roundRect(80, 200, PAGE_WIDTH - 160, 850, 25, fill=True, stroke=False)
    
    # Subtle border
    c.setStrokeColor(Color(1, 1, 1, alpha=0.5))
    c.setLineWidth(2)
    c.roundRect(80, 200, PAGE_WIDTH - 160, 850, 25, fill=False, stroke=True)
    
    # Load and draw persona image - MUCH BIGGER
    persona_img_path = os.path.join(PERSONA_DIR, f"{persona_key}.png")
    if os.path.exists(persona_img_path):
        img = Image.open(persona_img_path)
        img_reader = ImageReader(img)
        img_size = 650  # Much bigger
        c.drawImage(img_reader, (PAGE_WIDTH - img_size) / 2, 450, 
                    width=img_size, height=img_size, mask='auto')
    
    # Persona title - orange to match theme
    c.setFillColor(HexColor("#FF6A00"))
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(PAGE_WIDTH / 2, 400, persona['title'])
    
    # Persona description - dark text
    c.setFillColor(HexColor("#333333"))
    c.setFont("Helvetica-Bold", 26)
    
    # Word wrap description
    words = persona['desc'].split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(' '.join(current_line)) > 35:
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(' '.join(current_line))
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    
    y_pos = 320
    for line in lines:
        c.drawCentredString(PAGE_WIDTH / 2, y_pos, line)
        y_pos -= 40
    
    # Stats at bottom
    c.setFillColor(HexColor("#666666"))
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(PAGE_WIDTH / 2, 230, 
                        f"Based on {data['total_conversations']:,} conversations in 2025")
    
    c.save()
    packet.seek(0)
    return packet

if __name__ == "__main__":
    from pypdf import PdfReader
    overlay = create_overlay()
    reader = PdfReader(overlay)
    print(f"Page 11 overlay created")
