from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
from scraper import get_events  # move your Playwright scraper to scraper.py
import threading

app = Flask(__name__)

# In-memory cache
cached_events = []
last_scraped = None
cache_duration = timedelta(minutes=10)

def update_cache():
    global cached_events, last_scraped
    print("Scraping events...")
    try:
        cached_events = get_events()
        last_scraped = datetime.now()
        print(f"Cached {len(cached_events)} events.")
    except Exception as e:
        print("Scraping failed:", e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/events')
def events():
    global last_scraped
    now = datetime.now()

    if not cached_events or not last_scraped or now - last_scraped > cache_duration:
        # Scrape in a background thread to avoid freezing page load
        thread = threading.Thread(target=update_cache)
        thread.start()
    
    return jsonify(cached_events)

@app.route('/log_email', methods=['POST'])
def log_email():
    data = request.json
    email = data.get('email')
    link = data.get('link')

    if not email or '@' not in email:
        return jsonify({'status': 'skipped', 'message': 'Email not provided'}), 200

    with open('emails.csv', 'a') as f:
        f.write(f"{email},{link}\n")

    print(f"Logged: {email} for {link}")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    update_cache()  # Initial load
    app.run(debug=True)
