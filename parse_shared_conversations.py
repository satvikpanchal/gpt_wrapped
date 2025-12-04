#!/usr/bin/env python3
"""
GPT Wrapped: Shared Conversations Parser
Visualize your shared ChatGPT conversations in the terminal
"""

import json
from pathlib import Path

# Hardcoded path to the shared conversations file
DATA_PATH = "51f364fa5a7837c908187fdb2f76ed29f4b3ca825902b01b83b0450feb257ac1-2025-12-04-05-31-50-95251bd2a47f433c9bd2eea0dbba91bf/shared_conversations.json"


def load_shared_conversations(filepath: str) -> list:
    """Load and parse the shared conversations JSON file."""
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)


def print_header():
    """Print a stylish header for the output."""
    print("\n" + "=" * 60)
    print("🎵 GPT WRAPPED: YOUR SHARED CONVERSATIONS 🎵")
    print("=" * 60)


def print_conversation(index: int, conv: dict):
    """Print a single conversation entry with formatting."""
    print(f"\n📌 #{index + 1}")
    print(f"   Title:          {conv.get('title', 'Untitled')}")
    print(f"   Share ID:       {conv.get('id', 'N/A')}")
    print(f"   Conversation:   {conv.get('conversation_id', 'N/A')}")
    print(f"   Anonymous:      {'✅ Yes' if conv.get('is_anonymous') else '❌ No'}")


def print_summary(conversations: list):
    """Print summary statistics."""
    total = len(conversations)
    anonymous_count = sum(1 for c in conversations if c.get("is_anonymous"))
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY STATS")
    print("=" * 60)
    print(f"   Total Shared Conversations:    {total}")
    print(f"   Anonymous Shares:              {anonymous_count}")
    print(f"   Public Shares:                 {total - anonymous_count}")
    print("=" * 60 + "\n")


def main():
    """Main entrypoint for the shared conversations parser."""
    filepath = Path(DATA_PATH)
    
    if not filepath.exists():
        print(f"❌ Error: File not found at {filepath}")
        return
    
    conversations = load_shared_conversations(filepath)
    
    print_header()
    
    for idx, conv in enumerate(conversations):
        print_conversation(idx, conv)
    
    print_summary(conversations)


if __name__ == "__main__":
    main()

