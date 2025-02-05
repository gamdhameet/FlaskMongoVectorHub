from playwright.sync_api import sync_playwright
import csv
from urllib.parse import urljoin
import time

def scrape_tamu():
    # Create a global set to track common site-wide content
    global_content_set = set()

    # Create a CSV file to store the scraped data
    openpathcsv = 'tamu_football_filtered_data.csv'
    with open(openpathcsv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["URL", "Title", "Specific Content"])  # Header row

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Set a user-agent to mimic a real browser
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            })

            start_url = "https://12thman.com/sports/football"
            visited_urls = set()
            urls_to_scrape = [start_url]

            while urls_to_scrape:
                current_url = urls_to_scrape.pop(0)
                if current_url in visited_urls:
                    continue

                print(f"Scraping: {current_url}")
                try:
                    page.goto(current_url, wait_until="domcontentloaded", timeout=15000)
                    title = page.title()
                    paragraphs = page.eval_on_selector_all("p", "elements => elements.map(el => el.innerText)")
                    content = [line.strip() for line in paragraphs if line.strip()]

                    # Identify specific content by filtering out shared/global content
                    specific_content = []
                    for line in content:
                        if line not in global_content_set:
                            specific_content.append(line)
                            global_content_set.add(line)  # Add to global set

                    if specific_content:
                        writer.writerow([current_url, title, " ".join(specific_content)])

                    visited_urls.add(current_url)

                    # Extract and queue new links
                    links = page.eval_on_selector_all("a", "elements => elements.map(el => el.href)")
                    for link in links:
                        absolute_url = urljoin(current_url, link)
                        if absolute_url.startswith(start_url) and absolute_url not in visited_urls:
                            urls_to_scrape.append(absolute_url)

                    # Add a small delay to reduce server load
                    time.sleep(1)

                except Exception as e:
                    print(f"Error scraping {current_url}: {e}")
                    continue

            browser.close()

if __name__ == "__main__":
    scrape_tamu()