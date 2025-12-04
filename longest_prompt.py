#!/usr/bin/env python3
"""
GPT Wrapped: Longest Prompt Finder
Find the longest messages you've sent to ChatGPT
"""

import json
from pathlib import Path
from datetime import datetime

# Hardcoded path to the conversations file
DATA_PATH = "51f364fa5a7837c908187fdb2f76ed29f4b3ca825902b01b83b0450feb257ac1-2025-12-04-05-31-50-95251bd2a47f433c9bd2eea0dbba91bf/conversations.json"

# Date filter: Only include conversations from 2025 onwards
START_DATE = datetime(2025, 1, 1, 0, 0, 0).timestamp()

TOP_N = 10
PREVIEW_LENGTH = 500  # Characters to preview


def load_conversations(filepath: str) -> list:
    """Load and parse the conversations JSON file."""
    print(f"📂 Loading {filepath}...")
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)


def filter_by_date(conversations: list) -> list:
    """Filter conversations to only include those from 2025 onwards."""
    filtered = [c for c in conversations if c.get("create_time", 0) >= START_DATE]
    return filtered


def format_timestamp(ts: float) -> str:
    """Convert Unix timestamp to readable date."""
    if ts is None:
        return "Unknown"
    try:
        return datetime.fromtimestamp(ts).strftime("%Y/%m/%d %H:%M")
    except (ValueError, OSError):
        return "Invalid date"


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
            text = part.get("text", "")
            if text:
                text_parts.append(text)
    
    return " ".join(text_parts)


def find_longest_prompts(conversations: list) -> list:
    """Find the longest user prompts across all conversations."""
    prompts = []
    
    for conv in conversations:
        title = conv.get("title", "Untitled")
        created = conv.get("create_time")
        mapping = conv.get("mapping", {})
        
        for node in mapping.values():
            message = node.get("message")
            if message:
                role = message.get("author", {}).get("role", "")
                if role == "user":
                    text = extract_text_from_message(message)
                    if text:
                        prompts.append({
                            "text": text,
                            "length": len(text),
                            "word_count": len(text.split()),
                            "title": title,
                            "timestamp": created,
                        })
    
    # Sort by length descending
    prompts.sort(key=lambda x: x["length"], reverse=True)
    return prompts[:TOP_N]


def print_results(prompts: list):
    """Print the longest prompts in a nice format."""
    print("\n" + "=" * 70)
    print("📏 TOP 10 LONGEST PROMPTS YOU SENT (2025 Only)")
    print("=" * 70)
    
    for rank, prompt in enumerate(prompts, 1):
        chars = prompt["length"]
        words = prompt["word_count"]
        title = prompt["title"]
        date = format_timestamp(prompt["timestamp"])
        preview = prompt["text"][:PREVIEW_LENGTH]
        
        # Clean up preview
        preview = preview.replace("\n", " ").strip()
        if len(prompt["text"]) > PREVIEW_LENGTH:
            preview += "..."
        
        print(f"\n🏆 #{rank}")
        print(f"   📊 Length:    {chars:,} characters | {words:,} words")
        print(f"   💬 Chat:      {title}")
        print(f"   📅 Date:      {date}")
        print(f"   📝 Preview:")
        
        # Word wrap the preview
        words_list = preview.split()
        line = "      "
        for word in words_list:
            if len(line) + len(word) + 1 > 75:
                print(line)
                line = "      " + word
            else:
                line += " " + word if line.strip() else word
        if line.strip():
            print(line)
    
    print("\n" + "=" * 70)


def print_stats(prompts: list, all_prompts_count: int):
    """Print summary statistics."""
    if not prompts:
        return
    
    longest = prompts[0]
    print(f"\n📈 STATS")
    print(f"   Longest prompt: {longest['length']:,} characters")
    print(f"   That's about {longest['length'] // 250} pages of text!")
    print(f"   Total prompts analyzed: {all_prompts_count:,}")


def main():
    """Main entrypoint."""
    filepath = Path(DATA_PATH)
    
    if not filepath.exists():
        print(f"❌ Error: File not found at {filepath}")
        return
    
    all_conversations = load_conversations(filepath)
    conversations = filter_by_date(all_conversations)
    print(f"✅ Filtered to {len(conversations):,} conversations from 2025")
    
    print("\n⏳ Finding longest prompts...")
    
    # Get all prompts for count
    all_prompts = []
    for conv in conversations:
        mapping = conv.get("mapping", {})
        for node in mapping.values():
            message = node.get("message")
            if message and message.get("author", {}).get("role") == "user":
                text = extract_text_from_message(message)
                if text:
                    all_prompts.append(text)
    
    longest = find_longest_prompts(conversations)
    print_results(longest)
    print_stats(longest, len(all_prompts))


if __name__ == "__main__":
    main()

