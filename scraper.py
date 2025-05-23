import json
from playwright.sync_api import sync_playwright
from datetime import datetime

def get_events():
    events = []
    seen_links = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ))
        page = context.new_page()

        try:
            print("⏳ Navigating to Eventbrite...")
            page.goto("https://www.eventbrite.com.au/d/australia--sydney/events/", timeout=90000)
            page.wait_for_timeout(10000)  # give JS time to render
        except Exception as e:
            print(f"❌ Page failed to load: {e}")
            page.screenshot(path="debug-goto-fail.png", full_page=True)
            return []

        cards = page.query_selector_all("a.event-card-link")
        print(f"✅ Found {len(cards)} cards")


        for card in cards:
            try:
                link = card.get_attribute("href")
                location = card.get_attribute("data-event-location") or "Sydney"
                image_el = card.query_selector("img.event-card-image")
                image = image_el.get_attribute("src") if image_el else ""
                aria_label = card.get_attribute("aria-label") or ""
                title = aria_label.replace("View ", "").strip()

                if not title or not link or link in seen_links:
                    continue

                seen_links.add(link)

                events.append({
                    "title": title,
                    "date": "Upcoming",
                    "location": location,
                    "link": link,
                    "image": image
                })

            except Exception as e:
                print("⚠️ Error parsing card:", e)

        browser.close()
    return events

def save_events_to_json(path="events.json"):
    events = get_events()
    data = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "events": events
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved {len(events)} events to {path} at {data['last_updated']}")

if __name__ == "__main__":
    save_events_to_json()
