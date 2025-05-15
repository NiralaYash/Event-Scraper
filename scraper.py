from playwright.sync_api import sync_playwright


def get_events():
    events = []
    seen_links = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.eventbrite.com.au/d/australia--sydney/events/", timeout=60000)

        page.wait_for_timeout(8000)
        page.screenshot(path="sydney_events.png", full_page=True)

        cards = page.query_selector_all('a.event-card-link')
        print(f"Found {len(cards)} event cards")

        for card in cards:
            try:
                title_el = card.query_selector('h3')
                title = title_el.inner_text().strip() if title_el else None
                link = card.get_attribute("href").strip()
                location = card.get_attribute("data-event-location") or "Sydney"

                # Skip cards with missing titles or already seen links
                if not title or link in seen_links:
                    continue

                seen_links.add(link)

                events.append({
                    "title": title,
                    "date": "Upcoming",
                    "location": location,
                    "link": link
                })

            except Exception as e:
                print("Failed to parse event:", e)
                continue

        browser.close()

    return events

# Run it
if __name__ == "__main__":
    for event in get_events():
        print(event)
