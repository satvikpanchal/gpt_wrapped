#!/usr/bin/env python3
"""
GPT Wrapped: Model Usage Pie Chart
Visualize which GPT models you used throughout 2025
"""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend for saving files
import matplotlib.pyplot as plt

# Hardcoded path to the conversations file
DATA_PATH = "51f364fa5a7837c908187fdb2f76ed29f4b3ca825902b01b83b0450feb257ac1-2025-12-04-05-31-50-95251bd2a47f433c9bd2eea0dbba91bf/conversations.json"

# Date filter: Only include conversations from 2025 onwards
START_DATE = datetime(2025, 1, 1, 0, 0, 0).timestamp()

# Output file
OUTPUT_FILE = "model_usage_2025.png"


def load_conversations(filepath: str) -> list:
    """Load and parse the conversations JSON file."""
    print(f"📂 Loading {filepath}...")
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)


def filter_by_date(conversations: list) -> list:
    """Filter conversations to only include those from 2025 onwards."""
    filtered = [c for c in conversations if c.get("create_time", 0) >= START_DATE]
    return filtered


def count_models(conversations: list) -> Counter:
    """Count model usage across conversations."""
    models = Counter()
    for conv in conversations:
        model = conv.get("default_model_slug", "unknown")
        if model:
            models[model] += 1
        else:
            models["unknown"] += 1
    return models


def create_pie_chart(model_counts: Counter, total: int):
    """Create a beautiful pie chart of model usage."""
    
    # Sort by count descending
    sorted_models = model_counts.most_common()
    
    # Group small slices (< 2%) into "Other"
    threshold = total * 0.02
    main_models = []
    other_count = 0
    
    for model, count in sorted_models:
        if count >= threshold:
            main_models.append((model, count))
        else:
            other_count += count
    
    if other_count > 0:
        main_models.append(("Other", other_count))
    
    labels = [m[0] for m in main_models]
    sizes = [m[1] for m in main_models]
    percentages = [(s / total) * 100 for s in sizes]
    
    # Color palette (vibrant and modern)
    colors = [
        "#FF6B6B",  # Coral red
        "#4ECDC4",  # Teal
        "#45B7D1",  # Sky blue
        "#96CEB4",  # Sage green
        "#FFEAA7",  # Soft yellow
        "#DDA0DD",  # Plum
        "#98D8C8",  # Mint
        "#F7DC6F",  # Gold
        "#BB8FCE",  # Lavender
        "#85C1E9",  # Light blue
        "#F8B500",  # Amber
        "#C0C0C0",  # Silver (for Other)
    ]
    
    # Create figure with dark background for that Wrapped feel
    fig, ax = plt.subplots(figsize=(12, 8), facecolor="#1a1a2e")
    ax.set_facecolor("#1a1a2e")
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct=lambda pct: f'{pct:.1f}%' if pct > 3 else '',
        colors=colors[:len(sizes)],
        explode=[0.02] * len(sizes),
        shadow=True,
        startangle=90,
        textprops={'color': 'white', 'fontsize': 12, 'fontweight': 'bold'}
    )
    
    # Style the percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    # Add title
    ax.set_title(
        "🤖 GPT Models You Used in 2025",
        fontsize=20,
        fontweight='bold',
        color='white',
        pad=20
    )
    
    # Create legend with counts
    legend_labels = [
        f"{label}: {count:,} ({pct:.1f}%)"
        for label, count, pct in zip(labels, sizes, percentages)
    ]
    
    legend = ax.legend(
        wedges,
        legend_labels,
        title="Models",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=11,
        title_fontsize=13,
        facecolor="#16213e",
        edgecolor="white",
        labelcolor="white"
    )
    legend.get_title().set_color('white')
    
    # Add total conversations text
    ax.text(
        0, -1.4,
        f"Total Conversations: {total:,}",
        ha='center',
        fontsize=14,
        color='white',
        fontweight='bold'
    )
    
    plt.tight_layout()
    
    # Save the chart
    plt.savefig(
        OUTPUT_FILE,
        dpi=150,
        facecolor="#1a1a2e",
        edgecolor='none',
        bbox_inches='tight'
    )
    print(f"✅ Saved pie chart to {OUTPUT_FILE}")
    print(f"📂 Open the file to view: open {OUTPUT_FILE}")


def print_table(model_counts: Counter, total: int):
    """Print a text table of model usage."""
    print("\n" + "=" * 50)
    print("🤖 MODEL USAGE BREAKDOWN (2025)")
    print("=" * 50)
    print(f"   {'Model':<20} {'Count':>8} {'Percent':>10}")
    print("   " + "─" * 42)
    
    for model, count in model_counts.most_common():
        pct = (count / total) * 100
        bar = "█" * int(pct / 2)
        print(f"   {model:<20} {count:>8} {pct:>9.1f}%")
    
    print("   " + "─" * 42)
    print(f"   {'TOTAL':<20} {total:>8} {'100.0%':>10}")
    print("=" * 50)


def main():
    """Main entrypoint."""
    filepath = Path(DATA_PATH)
    
    if not filepath.exists():
        print(f"❌ Error: File not found at {filepath}")
        return
    
    all_conversations = load_conversations(filepath)
    conversations = filter_by_date(all_conversations)
    total = len(conversations)
    print(f"✅ Filtered to {total:,} conversations from 2025")
    
    # Count models
    model_counts = count_models(conversations)
    
    # Print text table
    print_table(model_counts, total)
    
    # Create pie chart
    print("\n📊 Generating pie chart...")
    create_pie_chart(model_counts, total)


if __name__ == "__main__":
    main()

