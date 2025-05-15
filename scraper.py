from playwright.sync_api import sync_playwright

def get_events():
    events = []
    seen_links = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.eventbrite.com.au/d/australia--sydney/events/", timeout=60000)

        try:
            page.wait_for_selector('a.event-card-link', timeout=10000)
        except Exception as e:
            print("Timeout waiting for event cards:", e)
            return []

        cards = page.query_selector_all('a.event-card-link')
        print(f"Found {len(cards)} event cards")

        for card in cards:
            try:
                link = card.get_attribute("href")
                location = card.get_attribute("data-event-location") or "Sydney"
                image_el = card.query_selector('img.event-card-image')
                image = image_el.get_attribute("src") if image_el else ""

                # Extract title from aria-label and clean it
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
                print("Error parsing card:", e)
                continue

        browser.close()

    return events

# Run it
if __name__ == "__main__":
    for event in get_events():
        print(event)
