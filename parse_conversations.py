#!/usr/bin/env python3
"""
GPT Wrapped: Conversations Parser
Analyze your ChatGPT conversation history with configurable limits
"""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter

# Hardcoded path to the conversations file
DATA_PATH = "51f364fa5a7837c908187fdb2f76ed29f4b3ca825902b01b83b0450feb257ac1-2025-12-04-05-31-50-95251bd2a47f433c9bd2eea0dbba91bf/conversations.json"

# Configuration: How many conversations to display in detail
DISPLAY_LIMIT = 10

# Date filter: Only include conversations from 2025 onwards
START_DATE = datetime(2025, 1, 1, 0, 0, 0).timestamp()


def load_conversations(filepath: str) -> list:
    """Load and parse the conversations JSON file."""
    print(f"📂 Loading {filepath}...")
    with open(filepath, "r", encoding="utf8") as f:
        data = json.load(f)
    return data


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


def count_messages(mapping: dict) -> tuple[int, int]:
    """Count user and assistant messages from the mapping."""
    user_count = 0
    assistant_count = 0
    
    if not mapping:
        return 0, 0
    
    for node in mapping.values():
        message = node.get("message")
        if message:
            role = message.get("author", {}).get("role", "")
            if role == "user":
                user_count += 1
            elif role == "assistant":
                assistant_count += 1
    
    return user_count, assistant_count


def print_header(total_count: int, file_size_mb: float):
    """Print a stylish header with file stats."""
    print("\n" + "=" * 70)
    print("🎵 GPT WRAPPED 2025: YOUR CONVERSATION HISTORY 🎵")
    print("=" * 70)
    print(f"📅 Date Range: Jan 1, 2025 → Present")
    print(f"📊 Total Conversations: {total_count:,}")
    print(f"💾 File Size: {file_size_mb:.1f} MB")
    print(f"🔍 Showing: First {DISPLAY_LIMIT} conversations")
    print("=" * 70)


def print_conversation(index: int, conv: dict):
    """Print a single conversation with key details."""
    title = conv.get("title", "Untitled")
    created = format_timestamp(conv.get("create_time"))
    updated = format_timestamp(conv.get("update_time"))
    model = conv.get("default_model_slug", "Unknown")
    archived = "📦 Archived" if conv.get("is_archived") else ""
    
    user_msgs, assistant_msgs = count_messages(conv.get("mapping", {}))
    total_msgs = user_msgs + assistant_msgs
    
    print(f"\n📌 #{index + 1}: {title}")
    print(f"   Created:    {created}")
    print(f"   Updated:    {updated}")
    print(f"   Model:      {model}")
    print(f"   Messages:   {total_msgs} ({user_msgs} user, {assistant_msgs} assistant)")
    if archived:
        print(f"   Status:     {archived}")


def print_summary(conversations: list):
    """Print comprehensive summary statistics."""
    total = len(conversations)
    
    # Count models used
    models = Counter(c.get("default_model_slug", "unknown") for c in conversations)
    
    # Count archived
    archived_count = sum(1 for c in conversations if c.get("is_archived"))
    
    # Count total messages
    total_user = 0
    total_assistant = 0
    for conv in conversations:
        u, a = count_messages(conv.get("mapping", {}))
        total_user += u
        total_assistant += a
    
    # Get date range
    timestamps = [c.get("create_time") for c in conversations if c.get("create_time")]
    if timestamps:
        earliest = format_timestamp(min(timestamps))
        latest = format_timestamp(max(timestamps))
    else:
        earliest = latest = "Unknown"
    
    print("\n" + "=" * 70)
    print("📈 FULL SUMMARY STATS (All Conversations)")
    print("=" * 70)
    print(f"   Total Conversations:      {total:,}")
    print(f"   Total Messages:           {total_user + total_assistant:,}")
    print(f"      • Your Messages:       {total_user:,}")
    print(f"      • GPT Responses:       {total_assistant:,}")
    print(f"   Archived:                 {archived_count:,}")
    print(f"   Date Range:               {earliest} → {latest}")
    print()
    print("   🤖 Models Used:")
    for model, count in models.most_common(10):
        pct = (count / total) * 100
        print(f"      • {model or 'unknown'}: {count:,} ({pct:.1f}%)")
    print("=" * 70 + "\n")


def main():
    """Main entrypoint for the conversations parser."""
    filepath = Path(DATA_PATH)
    
    if not filepath.exists():
        print(f"❌ Error: File not found at {filepath}")
        return
    
    # Get file size
    file_size_mb = filepath.stat().st_size / (1024 * 1024)
    
    # Load all conversations and filter by date
    all_conversations = load_conversations(filepath)
    conversations = filter_by_date(all_conversations)
    print(f"✅ Filtered to {len(conversations):,} conversations from 2025")
    
    print_header(len(conversations), file_size_mb)
    
    # Display limited number of conversations
    for idx, conv in enumerate(conversations[:DISPLAY_LIMIT]):
        print_conversation(idx, conv)
    
    if len(conversations) > DISPLAY_LIMIT:
        print(f"\n   ... and {len(conversations) - DISPLAY_LIMIT:,} more conversations")
    
    # Full summary uses ALL data
    print_summary(conversations)


if __name__ == "__main__":
    main()

