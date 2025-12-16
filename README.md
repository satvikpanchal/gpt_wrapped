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

### Step 1: Export Your ChatGPT Data

1. Go to https://chat.openai.com
2. Click your profile icon in the bottom-left corner
3. Click **Settings**
4. Go to **Data Controls**
5. Click **Export Data**
6. Confirm by clicking **Export**
7. Wait for an email from OpenAI (usually takes a few minutes)
8. Download the zip file from the email link
9. Unzip the file - you'll find a folder containing `conversations.json`

### Step 2: Clone or Download This Project

```bash
git clone https://github.com/YOUR_USERNAME/gpt_wrapped.git
cd gpt_wrapped
```

Or download and extract the ZIP file.

### Step 3: Set Up Python Environment

Make sure you have Python 3.8 or higher installed.

```bash
# Check your Python version
python --version

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Your Data Path

Open `data_extractor.py` in any text editor and update the `DATA_FILE` path to point to your `conversations.json` file:

```python
DATA_FILE = "path/to/your/conversations.json"
```

For example:
- macOS: `DATA_FILE = "/Users/yourname/Downloads/chatgpt-export/conversations.json"`
- Windows: `DATA_FILE = "C:/Users/yourname/Downloads/chatgpt-export/conversations.json"`
- Or just copy the conversations.json to this folder and use: `DATA_FILE = "conversations.json"`

### Step 6: Generate Your Wrapped

```bash
python compile_pdf.py
```

### Step 7: View Your Results

Open `gpt_wrapped_2025_final.pdf` - that's your personalized GPT Wrapped!

---

## Troubleshooting

### "FileNotFoundError: conversations.json"
- Make sure the path in `data_extractor.py` points to your actual `conversations.json` file
- Try using an absolute path (full path starting from root)

### "No module named 'PIL'" or similar
- Make sure you activated the virtual environment: `source venv/bin/activate`
- Run `pip install -r requirements.txt` again

### "Template has 0 pages" or PDF errors
- Make sure `GPT_WRAPPED_TEMPLATE.pdf` exists in the project folder
- Don't rename or move the template file

### Charts look wrong or data seems off
- Make sure your `conversations.json` is from a recent ChatGPT export
- The script filters for 2025 conversations by default

---

## Project Structure

```
gpt_wrapped/
├── compile_pdf.py              # Main script - runs everything
├── data_extractor.py           # Extracts stats from conversations.json
├── GPT_WRAPPED_TEMPLATE.pdf    # Template PDF with backgrounds
├── requirements.txt            # Python dependencies
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
CUTOFF = datetime(2024, 1, 1)  # Change to 2024 or any year
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
- pillow >= 10.0.0
- reportlab >= 4.0.0
- pypdf >= 3.0.0
- matplotlib >= 3.7.0
- numpy >= 1.24.0

---

## Stats Tracked

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

## License

MIT License - Use it, modify it, share it.

---

**Made for the ChatGPT community**
