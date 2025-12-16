# GPT Wrapped 2025

Generate your own Spotify Wrapped-style recap of your ChatGPT usage. See your stats, streaks, favorite words, and more in a beautifully designed PDF.

---

## Features

- **Total Stats** - Words sent/received, messages exchanged, conversations started
- **Longest Streak** - Your most consistent ChatGPT usage period
- **Top Words** - Your 10 most frequently used words
- **Model Usage** - Pie chart of which GPT models you used
- **Longest Chat** - Your marathon conversation topic
- **Monthly Activity** - Bar chart of conversations per month
- **Activity Heatmap** - When you chat the most (by hour/day)
- **GPT Persona** - What kind of GPT user are you?
- **Summary Dashboard** - All your key stats in one polished view

---

## Quick Start

### 1. Export Your ChatGPT Data

1. Go to [ChatGPT](https://chat.openai.com)
2. Click your profile, then Settings
3. Data Controls, then Export Data
4. Wait for the email, download and unzip

You'll get a folder containing `conversations.json` - that's what we need.

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install pillow reportlab pypdf matplotlib numpy
```

### 3. Configure Your Data Path

Open `data_extractor.py` and update the path to your conversations file:

```python
DATA_FILE = "/path/to/your/conversations.json"
```

### 4. Generate Your Wrapped

```bash
python compile_pdf.py
```

Your personalized recap will be saved as `gpt_wrapped_2025_final.pdf`

---

## Project Structure

```
gpt_wrapped/
├── compile_pdf.py              # Main script - runs everything
├── data_extractor.py           # Extracts stats from conversations.json
├── GPT_WRAPPED_TEMPLATE.pdf    # Template PDF with backgrounds
├── extracted_data.pkl          # Cached stats (auto-generated)
├── gpt_wrapped_2025_final.pdf  # Your output
│
├── page3_words.py              # Word count overlay
├── page4_streak.py             # Streak + dates overlay
├── page5_top_words.py          # Top 10 words overlay
├── page6_pie_chart.py          # Model usage pie chart
├── page7_longest_chat.py       # Longest conversation overlay
├── page8_monthly_chart.py      # Monthly activity bar chart
├── page9_heatmap.py            # Hourly activity heatmap
├── page10_prompts.py           # Longest prompts list
├── page11_persona.py           # GPT persona/personality
├── page12_summary.py           # Summary dashboard
│
└── gpt_persona/                # Persona images
    ├── researcher.png
    ├── builder.png
    └── ...
```

---

## Customization

### Change the Year Filter

By default, it filters for 2025 conversations. To change this, edit `data_extractor.py`:

```python
CUTOFF = datetime(2025, 1, 1)  # Change year here
```

### Modify Page Layouts

Each `pageX_*.py` file controls one page's overlay. Key variables:
- `PAGE_WIDTH = 810`
- `PAGE_HEIGHT = 1440`
- Coordinates: `y=0` is bottom, `y=1440` is top

### Use a Different Template

Replace `GPT_WRAPPED_TEMPLATE.pdf` with your own 13-page template PDF, then adjust the overlay positions in each page file.

---

## Requirements

- Python 3.8+
- PIL/Pillow
- ReportLab
- PyPDF
- Matplotlib
- NumPy

---

## What Stats Are Tracked?

| Stat | Description |
|------|-------------|
| `user_words` | Total words you typed |
| `gpt_words` | Total words GPT wrote back |
| `user_messages` | Number of messages you sent |
| `gpt_messages` | Number of GPT responses |
| `total_conversations` | Conversation count |
| `longest_streak` | Max consecutive days of usage |
| `top_words` | Your 10 most-used words (excluding common words) |
| `model_usage` | Breakdown of GPT-4, GPT-4o, etc. |
| `monthly_activity` | Conversations per month |
| `hourly_activity` | Activity by hour of day |
| `longest_chat_title` | Your longest conversation topic |
| `longest_chat_messages` | Message count in that chat |

---

## Contributing

Feel free to:
- Add new page designs
- Improve the statistics extraction
- Create alternative templates
- Add more visualization types

---

## License

MIT License - Use it, modify it, share it.

---

**Made for the ChatGPT community**

See you next year!
