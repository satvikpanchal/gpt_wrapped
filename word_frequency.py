#!/usr/bin/env python3
"""
GPT Wrapped: Word Frequency Analyzer
Find your most used words across all conversations
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

# Hardcoded path to the conversations file
DATA_PATH = "51f364fa5a7837c908187fdb2f76ed29f4b3ca825902b01b83b0450feb257ac1-2025-12-04-05-31-50-95251bd2a47f433c9bd2eea0dbba91bf/conversations.json"

# Date filter: Only include conversations from 2025 onwards
START_DATE = datetime(2025, 1, 1, 0, 0, 0).timestamp()

# Common stopwords to exclude
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
    "be", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "shall", "can", "need",
    "it", "its", "this", "that", "these", "those", "i", "you", "he",
    "she", "we", "they", "what", "which", "who", "whom", "how", "when",
    "where", "why", "all", "each", "every", "both", "few", "more", "most",
    "other", "some", "such", "no", "not", "only", "own", "same", "so",
    "than", "too", "very", "just", "also", "now", "here", "there", "then",
    "if", "about", "into", "through", "during", "before", "after", "above",
    "below", "between", "under", "again", "further", "once", "any", "up",
    "down", "out", "off", "over", "your", "my", "me", "him", "her", "us",
    "them", "our", "their", "his", "hers", "yours", "ours", "theirs", "am",
    "being", "because", "until", "while", "let", "s", "t", "don", "doesn",
    "didn", "won", "wouldn", "couldn", "shouldn", "ll", "ve", "re", "d", "m",
    "like", "get", "make", "use", "using", "used", "one", "two", "first",
    "new", "way", "want", "see", "know", "think", "take", "come", "go",
}

TOP_N = 10


def load_conversations(filepath: str) -> list:
    """Load and parse the conversations JSON file."""
    print(f"📂 Loading {filepath}...")
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)


def filter_by_date(conversations: list) -> list:
    """Filter conversations to only include those from 2025 onwards."""
    filtered = [c for c in conversations if c.get("create_time", 0) >= START_DATE]
    return filtered


def extract_text_from_message(message: dict) -> str:
    """Extract text content from a message object."""
    if not message:
        return ""
    
    content = message.get("content", {})
    parts = content.get("parts", [])
    
    text_parts = []
    for part in parts:
        if isinstance(part, str):
            text_parts.append(part)
        elif isinstance(part, dict):
            # Handle structured content
            text = part.get("text", "")
            if text:
                text_parts.append(text)
    
    return " ".join(text_parts)


def extract_all_text(conversations: list, user_only: bool = False) -> str:
    """Extract all text from conversations."""
    all_text = []
    
    for conv in conversations:
        mapping = conv.get("mapping", {})
        for node in mapping.values():
            message = node.get("message")
            if message:
                role = message.get("author", {}).get("role", "")
                if user_only and role != "user":
                    continue
                if role in ("user", "assistant"):
                    text = extract_text_from_message(message)
                    if text:
                        all_text.append(text)
    
    return " ".join(all_text)


def count_words(text: str) -> Counter:
    """Count word frequencies, excluding stopwords."""
    # Lowercase and extract words (letters only, 3+ chars)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Filter stopwords
    filtered = [w for w in words if w not in STOPWORDS]
    
    return Counter(filtered)


def print_results(counter: Counter, title: str):
    """Print top words in a nice format."""
    print("\n" + "=" * 60)
    print(f"🔤 {title} (2025 Only)")
    print("=" * 60)
    
    for rank, (word, count) in enumerate(counter.most_common(TOP_N), 1):
        bar = "█" * min(count // 500, 30)  # Visual bar
        print(f"  {rank:2}. {word:<15} {count:,} {bar}")
    
    print("=" * 60)


def main():
    """Main entrypoint."""
    filepath = Path(DATA_PATH)
    
    if not filepath.exists():
        print(f"❌ Error: File not found at {filepath}")
        return
    
    all_conversations = load_conversations(filepath)
    conversations = filter_by_date(all_conversations)
    print(f"✅ Filtered to {len(conversations):,} conversations from 2025")
    
    # All messages
    print("\n⏳ Analyzing all messages...")
    all_text = extract_all_text(conversations, user_only=False)
    all_counter = count_words(all_text)
    print_results(all_counter, "TOP 10 WORDS (All Messages)")
    
    # User messages only
    print("\n⏳ Analyzing your messages only...")
    user_text = extract_all_text(conversations, user_only=True)
    user_counter = count_words(user_text)
    print_results(user_counter, "TOP 10 WORDS (Your Messages Only)")
    
    # Total word count
    total_words = sum(all_counter.values())
    user_words = sum(user_counter.values())
    print(f"\n📊 Total words analyzed: {total_words:,}")
    print(f"📊 Your words: {user_words:,}")


if __name__ == "__main__":
    main()

