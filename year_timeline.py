#!/usr/bin/env python3
"""
GPT Wrapped: Year Timeline
See your journey through 2025, month by month
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

# Hardcoded path to the conversations file
DATA_PATH = "51f364fa5a7837c908187fdb2f76ed29f4b3ca825902b01b83b0450feb257ac1-2025-12-04-05-31-50-95251bd2a47f433c9bd2eea0dbba91bf/conversations.json"

# Date filter: Only include conversations from 2025 onwards
START_DATE = datetime(2025, 1, 1, 0, 0, 0).timestamp()

# Month names
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Month emojis for vibes
MONTH_EMOJIS = ["❄️", "💕", "🌸", "🌧️", "🌺", "☀️", "🏖️", "🔥", "🍂", "🎃", "🍁", "🎄"]


def load_conversations(filepath: str) -> list:
    """Load and parse the conversations JSON file."""
    print(f"📂 Loading {filepath}...")
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)


def filter_by_date(conversations: list) -> list:
    """Filter conversations to only include those from 2025 onwards."""
    filtered = [c for c in conversations if c.get("create_time", 0) >= START_DATE]
    return filtered


def extract_keywords_from_title(title: str) -> list:
    """Extract meaningful keywords from a conversation title."""
    if not title:
        return []
    
    # Lowercase and extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
    
    # Common stopwords to filter
    stopwords = {
        "the", "and", "for", "with", "how", "what", "why", "when", "where",
        "can", "help", "need", "want", "get", "make", "use", "using", "fix",
        "error", "issue", "problem", "question", "about", "from", "this",
        "that", "code", "file", "not", "working", "work", "does", "doesn",
    }
    
    return [w for w in words if w not in stopwords]


def group_by_month(conversations: list) -> dict:
    """Group conversations by month."""
    monthly = defaultdict(list)
    
    for conv in conversations:
        ts = conv.get("create_time")
        if ts:
            try:
                dt = datetime.fromtimestamp(ts)
                if dt.year == 2025:
                    month_key = dt.month
                    monthly[month_key].append(conv)
            except (ValueError, OSError):
                pass
    
    return monthly


def analyze_month_topics(conversations: list) -> tuple[list, int, Counter]:
    """Analyze the main topics for a month's conversations."""
    all_keywords = []
    title_counter = Counter()
    
    for conv in conversations:
        title = conv.get("title", "")
        keywords = extract_keywords_from_title(title)
        all_keywords.extend(keywords)
        
        # Also count full titles for finding themes
        if title:
            title_counter[title] += 1
    
    keyword_counter = Counter(all_keywords)
    return keyword_counter.most_common(15), len(conversations), title_counter


def generate_month_summary(keywords: list, titles: Counter) -> str:
    """Generate a human readable summary of the month's focus."""
    if not keywords:
        return "Quiet month"
    
    # Get top keywords
    top_words = [k[0] for k in keywords[:10]]
    
    # Theme detection based on keywords
    themes = []
    
    # Tech/Cloud themes
    if any(w in top_words for w in ["aws", "sqs", "s3", "lambda", "cloud", "ec2"]):
        themes.append("AWS & Cloud")
    if any(w in top_words for w in ["spark", "hadoop", "databricks", "pyspark"]):
        themes.append("Spark & Big Data")
    if any(w in top_words for w in ["docker", "kubernetes", "k8s", "container"]):
        themes.append("DevOps")
    
    # ML/AI themes
    if any(w in top_words for w in ["model", "training", "neural", "deep", "learning", "tensorflow", "pytorch"]):
        themes.append("Machine Learning")
    if any(w in top_words for w in ["data", "mining", "analysis", "analytics"]):
        themes.append("Data Mining")
    if any(w in top_words for w in ["fraud", "detection", "classification"]):
        themes.append("Fraud Detection")
    
    # Academic themes
    if any(w in top_words for w in ["homework", "assignment", "project", "class", "course"]):
        themes.append("Coursework")
    if any(w in top_words for w in ["paper", "research", "thesis"]):
        themes.append("Research")
    
    # Specific tech
    if any(w in top_words for w in ["python", "java", "javascript", "typescript"]):
        themes.append("Coding")
    if any(w in top_words for w in ["robot", "robotics", "ros", "simulation"]):
        themes.append("Robotics")
    if any(w in top_words for w in ["greengrass", "iot", "edge"]):
        themes.append("Edge Computing")
    
    # Life themes
    if any(w in top_words for w in ["startup", "business", "product", "launch"]):
        themes.append("Startup Mode")
    if any(w in top_words for w in ["interview", "job", "resume", "career"]):
        themes.append("Career Hunt")
    if any(w in top_words for w in ["relma", "scale", "growth"]):
        themes.append("Scaling Up")
    
    # Misc fun
    if any(w in top_words for w in ["recipe", "food", "cook"]):
        themes.append("Cooking")
    if any(w in top_words for w in ["spotify", "music", "wrapped"]):
        themes.append("Spotify Wrapped")
    if any(w in top_words for w in ["party", "event", "planning"]):
        themes.append("Party Planning")
    
    if themes:
        return " + ".join(themes[:3])
    else:
        # Fall back to top keywords
        return " ".join(top_words[:3]).title()


def print_timeline(monthly_data: dict):
    """Print the beautiful emotional timeline."""
    print("\n" + "=" * 70)
    print("⭐ YOUR 2025 JOURNEY: A YEAR IN PROMPTS ⭐")
    print("=" * 70)
    print()
    
    total_convos = 0
    
    for month_num in range(1, 13):
        conversations = monthly_data.get(month_num, [])
        count = len(conversations)
        total_convos += count
        
        if count == 0:
            # Future month or no data
            if month_num <= datetime.now().month:
                print(f"   {MONTH_EMOJIS[month_num-1]} {MONTHS[month_num-1]:<12} │ (no conversations)")
            continue
        
        keywords, conv_count, titles = analyze_month_topics(conversations)
        summary = generate_month_summary(keywords, titles)
        
        # Create a mini bar for conversation count
        bar_len = min(count // 10, 20)
        bar = "▓" * bar_len
        
        print(f"   {MONTH_EMOJIS[month_num-1]} {MONTHS[month_num-1]:<12} │ {summary}")
        print(f"      {count:>4} chats   {bar}")
        
        # Show top 3 conversation titles as examples
        sample_titles = list(titles.keys())[:3]
        for title in sample_titles:
            short_title = title[:45] + "..." if len(title) > 45 else title
            print(f"                     └─ \"{short_title}\"")
        print()
    
    print("=" * 70)
    print(f"   📊 Total 2025 Conversations: {total_convos:,}")
    print("=" * 70)


def print_monthly_breakdown(monthly_data: dict):
    """Print detailed stats per month."""
    print("\n" + "=" * 70)
    print("📈 MONTHLY BREAKDOWN")
    print("=" * 70)
    print(f"   {'Month':<12} {'Chats':>8} {'Messages':>10} {'Avg/Chat':>10}")
    print("   " + "─" * 44)
    
    for month_num in range(1, 13):
        conversations = monthly_data.get(month_num, [])
        if not conversations:
            continue
        
        count = len(conversations)
        
        # Count messages
        total_msgs = 0
        for conv in conversations:
            mapping = conv.get("mapping", {})
            for node in mapping.values():
                msg = node.get("message")
                if msg and msg.get("author", {}).get("role") in ("user", "assistant"):
                    total_msgs += 1
        
        avg = total_msgs / count if count > 0 else 0
        
        print(f"   {MONTHS[month_num-1]:<12} {count:>8} {total_msgs:>10} {avg:>10.1f}")
    
    print("=" * 70)


def main():
    """Main entrypoint."""
    filepath = Path(DATA_PATH)
    
    if not filepath.exists():
        print(f"❌ Error: File not found at {filepath}")
        return
    
    all_conversations = load_conversations(filepath)
    conversations = filter_by_date(all_conversations)
    print(f"✅ Filtered to {len(conversations):,} conversations from 2025")
    
    # Group by month
    monthly_data = group_by_month(conversations)
    
    # Print the emotional timeline
    print_timeline(monthly_data)
    
    # Print monthly stats
    print_monthly_breakdown(monthly_data)


if __name__ == "__main__":
    main()

