#!/usr/bin/env python3
"""
Extract all analytics data from ChatGPT conversations for GPT Wrapped.
"""
import json
from datetime import datetime
from collections import Counter, defaultdict
import pickle

DATA_FILE = "51f364fa5a7837c908187fdb2f76ed29f4b3ca825902b01b83b0450feb257ac1-2025-12-04-05-31-50-95251bd2a47f433c9bd2eea0dbba91bf/conversations.json"
CUTOFF = datetime(2025, 1, 1)
OUTPUT_FILE = "extracted_data.pkl"

STOP_WORDS = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", 
              "is", "it", "that", "this", "with", "as", "be", "are", "was", "were", "been", 
              "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", 
              "should", "may", "might", "can", "i", "you", "he", "she", "we", "they", "my", 
              "your", "his", "her", "our", "their", "what", "which", "who", "how", "when", 
              "where", "why", "if", "then", "else", "not", "no", "yes", "so", "just", "like", 
              "more", "some", "any", "all", "also", "from", "by", "about", "into", "through", 
              "during", "before", "after", "above", "below", "between", "under", "over", 
              "out", "up", "down", "off", "such", "there", "here", "than", "its", "let", "me",
              "im", "dont", "cant", "wont", "youre", "theyre", "were", "ive", "use", "using",
              "want", "need", "get", "make", "know", "see", "think", "one", "two", "new"}

def load_conversations():
    """Load and filter conversations from 2025."""
    print("Loading conversations...")
    with open(DATA_FILE, "r") as f:
        conversations = json.load(f)
    
    filtered = []
    for c in conversations:
        if c.get("create_time"):
            ct = datetime.fromtimestamp(c["create_time"])
            if ct >= CUTOFF:
                filtered.append(c)
    
    print(f"Loaded {len(filtered)} conversations from 2025")
    return filtered

def extract_all_data(conversations):
    """Extract all analytics from conversations."""
    data = {}
    
    # Word counts
    user_words = 0
    gpt_words = 0
    user_messages = 0
    gpt_messages = 0
    
    # Word frequency
    all_user_words = []
    
    # Prompts for longest
    user_prompts = []
    
    # Model usage
    model_counts = Counter()
    
    # Hourly activity
    hourly_activity = defaultdict(int)
    
    # Monthly activity
    monthly_activity = defaultdict(int)
    
    # Daily activity for streak
    active_days = set()
    
    # Longest chat
    longest_chat = None
    max_messages = 0
    
    for c in conversations:
        # Get conversation date
        create_time = c.get("create_time")
        if create_time:
            dt = datetime.fromtimestamp(create_time)
            active_days.add(dt.date())
            hourly_activity[dt.hour] += 1
            monthly_activity[dt.month] += 1
        
        msg_count = 0
        for node_id, node in c.get("mapping", {}).items():
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
                user_prompts.append((word_count, c.get("title", "Untitled")))
                
                # Word frequency
                words = text.lower().split()
                for word in words:
                    cleaned = ''.join(ch for ch in word if ch.isalnum())
                    if cleaned and len(cleaned) > 2 and cleaned not in STOP_WORDS:
                        all_user_words.append(cleaned)
            
            elif role == "assistant":
                gpt_words += word_count
                gpt_messages += 1
                
                model = msg.get("metadata", {}).get("model_slug", "unknown")
                if model:
                    model_counts[model] += 1
        
        if msg_count > max_messages:
            max_messages = msg_count
            longest_chat = c
    
    # Calculate streak
    sorted_days = sorted(active_days)
    longest_streak = 0
    streak_start = None
    streak_end = None
    current_streak = 1
    current_start = sorted_days[0] if sorted_days else None
    
    for i in range(1, len(sorted_days)):
        diff = (sorted_days[i] - sorted_days[i-1]).days
        if diff == 1:
            current_streak += 1
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
                streak_start = current_start
                streak_end = sorted_days[i-1]
            current_streak = 1
            current_start = sorted_days[i]
    
    # Check final streak
    if current_streak > longest_streak:
        longest_streak = current_streak
        streak_start = current_start
        streak_end = sorted_days[-1] if sorted_days else None
    
    # Sort prompts
    user_prompts.sort(reverse=True)
    word_freq = Counter(all_user_words)
    
    data = {
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
    
    return data

def main():
    conversations = load_conversations()
    data = extract_all_data(conversations)
    
    print("\n=== GPT WRAPPED 2025 DATA ===")
    print(f"Words YOU → GPT: {data['user_words']:,}")
    print(f"Words GPT → YOU: {data['gpt_words']:,}")
    print(f"Messages sent: {data['user_messages']:,}")
    print(f"Messages received: {data['gpt_messages']:,}")
    print(f"Longest streak: {data['longest_streak']} days")
    if data['streak_start'] and data['streak_end']:
        print(f"  From: {data['streak_start'].strftime('%b %d')} → {data['streak_end'].strftime('%b %d')}")
    print(f"Longest chat: {data['longest_chat_title']} ({data['longest_chat_messages']} messages)")
    print(f"Top word: {data['top_words'][0][0]} ({data['top_words'][0][1]} times)")
    print(f"Top model: {data['model_usage'][0][0]}")
    
    # Save to pickle
    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(data, f)
    print(f"\nData saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()





