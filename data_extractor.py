#!/usr/bin/env python3
"""
GPT Wrapped Data Extractor

Parses your ChatGPT conversations.json export and extracts all the analytics
needed for generating your personalized GPT Wrapped report.
"""
import json
from datetime import datetime
from collections import Counter, defaultdict
import pickle

# Path to your ChatGPT data export (update this to your own file)
DATA_FILE = "51f364fa5a7837c908187fdb2f76ed29f4b3ca825902b01b83b0450feb257ac1-2025-12-04-05-31-50-95251bd2a47f433c9bd2eea0dbba91bf/conversations.json"

# Only include conversations from this year onwards
CUTOFF = datetime(2025, 1, 1)

# Where to save the extracted data
OUTPUT_FILE = "extracted_data.pkl"

# Common words to exclude from the "top words" analysis
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of",
    "is", "it", "that", "this", "with", "as", "be", "are", "was", "were", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "i", "you", "he", "she", "we", "they", "my",
    "your", "his", "her", "our", "their", "what", "which", "who", "how", "when",
    "where", "why", "if", "then", "else", "not", "no", "yes", "so", "just", "like",
    "more", "some", "any", "all", "also", "from", "by", "about", "into", "through",
    "during", "before", "after", "above", "below", "between", "under", "over",
    "out", "up", "down", "off", "such", "there", "here", "than", "its", "let", "me",
    "im", "dont", "cant", "wont", "youre", "theyre", "were", "ive", "use", "using",
    "want", "need", "get", "make", "know", "see", "think", "one", "two", "new"
}


def load_conversations():
    """
    Load the conversations.json file and filter to only include
    conversations created after the cutoff date.
    """
    print("Loading conversations...")
    with open(DATA_FILE, "r") as f:
        conversations = json.load(f)

    filtered = []
    for c in conversations:
        if c.get("create_time"):
            created = datetime.fromtimestamp(c["create_time"])
            if created >= CUTOFF:
                filtered.append(c)

    print(f"Loaded {len(filtered)} conversations from 2025")
    return filtered


def extract_all_data(conversations):
    """
    Process all conversations and extract analytics including:
    - Word and message counts
    - Most used words
    - Model usage breakdown
    - Activity patterns by hour and month
    - Longest usage streak
    - Longest conversation
    """
    
    # Counters for totals
    user_words = 0
    gpt_words = 0
    user_messages = 0
    gpt_messages = 0

    # Track all words the user typed for frequency analysis
    all_user_words = []

    # Track prompts to find the longest ones
    user_prompts = []

    # Count which GPT models were used
    model_counts = Counter()

    # Activity tracking
    hourly_activity = defaultdict(int)
    monthly_activity = defaultdict(int)
    active_days = set()

    # Track the conversation with the most messages
    longest_chat = None
    max_messages = 0

    for conversation in conversations:
        # Record when this conversation happened
        create_time = conversation.get("create_time")
        if create_time:
            dt = datetime.fromtimestamp(create_time)
            active_days.add(dt.date())
            hourly_activity[dt.hour] += 1
            monthly_activity[dt.month] += 1

        # Count messages in this conversation
        msg_count = 0
        
        for node_id, node in conversation.get("mapping", {}).items():
            msg = node.get("message")
            if not msg:
                continue

            role = msg.get("author", {}).get("role")
            parts = msg.get("content", {}).get("parts", [])
            text = " ".join(str(p) for p in parts if isinstance(p, str))

            if not text.strip():
                continue

            word_count = len(text.split())
            msg_count += 1

            if role == "user":
                user_words += word_count
                user_messages += 1
                user_prompts.append((word_count, conversation.get("title", "Untitled")))

                # Extract individual words for frequency analysis
                words = text.lower().split()
                for word in words:
                    cleaned = ''.join(ch for ch in word if ch.isalnum())
                    if cleaned and len(cleaned) > 2 and cleaned not in STOP_WORDS:
                        all_user_words.append(cleaned)

            elif role == "assistant":
                gpt_words += word_count
                gpt_messages += 1

                # Track which model generated this response
                model = msg.get("metadata", {}).get("model_slug", "unknown")
                if model:
                    model_counts[model] += 1

        # Check if this is the longest conversation so far
        if msg_count > max_messages:
            max_messages = msg_count
            longest_chat = conversation

    # Calculate the longest consecutive day streak
    sorted_days = sorted(active_days)
    longest_streak = 0
    streak_start = None
    streak_end = None
    current_streak = 1
    current_start = sorted_days[0] if sorted_days else None

    for i in range(1, len(sorted_days)):
        days_between = (sorted_days[i] - sorted_days[i - 1]).days
        if days_between == 1:
            # Consecutive day, extend the streak
            current_streak += 1
        else:
            # Gap in days, check if this was the longest streak
            if current_streak > longest_streak:
                longest_streak = current_streak
                streak_start = current_start
                streak_end = sorted_days[i - 1]
            current_streak = 1
            current_start = sorted_days[i]

    # Don't forget to check the final streak
    if current_streak > longest_streak:
        longest_streak = current_streak
        streak_start = current_start
        streak_end = sorted_days[-1] if sorted_days else None

    # Compile the final results
    user_prompts.sort(reverse=True)
    word_freq = Counter(all_user_words)

    return {
        "user_words": user_words,
        "gpt_words": gpt_words,
        "user_messages": user_messages,
        "gpt_messages": gpt_messages,
        "top_words": word_freq.most_common(10),
        "top_prompts": user_prompts[:10],
        "model_usage": model_counts.most_common(10),
        "hourly_activity": dict(hourly_activity),
        "monthly_activity": dict(monthly_activity),
        "longest_streak": longest_streak,
        "streak_start": streak_start,
        "streak_end": streak_end,
        "longest_chat_title": longest_chat.get("title", "Untitled") if longest_chat else "N/A",
        "longest_chat_messages": max_messages,
        "total_conversations": len(conversations),
    }


def main():
    """Load conversations, extract data, and save results."""
    conversations = load_conversations()
    data = extract_all_data(conversations)

    # Print a summary of what we found
    print("\n=== GPT WRAPPED 2025 DATA ===")
    print(f"Words you sent: {data['user_words']:,}")
    print(f"Words GPT sent: {data['gpt_words']:,}")
    print(f"Messages sent: {data['user_messages']:,}")
    print(f"Messages received: {data['gpt_messages']:,}")
    print(f"Longest streak: {data['longest_streak']} days")
    if data['streak_start'] and data['streak_end']:
        print(f"  From: {data['streak_start'].strftime('%b %d')} to {data['streak_end'].strftime('%b %d')}")
    print(f"Longest chat: {data['longest_chat_title']} ({data['longest_chat_messages']} messages)")
    print(f"Top word: {data['top_words'][0][0]} ({data['top_words'][0][1]} times)")
    print(f"Top model: {data['model_usage'][0][0]}")

    # Save the extracted data for the overlay generators to use
    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(data, f)
    print(f"\nData saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()






