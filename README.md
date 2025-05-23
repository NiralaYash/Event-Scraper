# Sydney Events Web App

A minimal full-stack web app that displays upcoming events in Sydney, with an optional email capture for tickets. Built using Flask, Playwright (for scraping), HTML, CSS, and JS.

---

## 🌐 Live Demo

Check out the working demo here:  
👉 [Sydney Events](https://event-scraper-cuxl.onrender.com/)

> Note: The live version uses cached event data (`events.json`) to avoid deployment issues with headless scraping.

---

## 🧪 Run Locally (with Live Scraping)

To run the app with live scraping and updated event data:

### 🔧 Requirements
- Python 3.10+
- [Playwright](https://playwright.dev/python/docs/intro) installed

### 🛠️ Steps

```bash
# Clone this repository
git clone https://github.com/yourusername/sydney-events-app.git
cd sydney-events-app

# Install dependencies
pip install -r requirements.txt
playwright install

# Run scraper to fetch fresh events
python scraper.py

# Start Flask server
python app.py
