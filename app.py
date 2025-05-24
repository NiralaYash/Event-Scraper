from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
import threading
import json
import os
from flask import make_response, jsonify
from scraper import save_events_to_json

app = Flask(__name__)

EVENT_FILE = "events.json"

# Run scraper on startup if possible
try:
    save_events_to_json(EVENT_FILE)
except Exception as e:
    print("⚠️ Scraper failed, falling back to cached data:", e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/api/events")
def events():
    try:
        with open("events.json", "r") as f:
            data = json.load(f)
        response = make_response(jsonify(data))
        response.headers["Cache-Control"] = "public, max-age=25200"  # 7 hours = 25200s
        return response
    except Exception as e:
        print("Failed to load events:", e)
        return jsonify([])

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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
