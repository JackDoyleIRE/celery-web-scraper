import time
import json
import requests
from bs4 import BeautifulSoup
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

MAX_DEPTH = 2

# Worker task that initiates the download and scrape process
@app.task
def worker(worker_name: str):
    print(f"Worker {worker_name} started.")
    # Start the initial requests with depth 0
    requests = [f"http://localhost:8000/sample_page.html" for i in range(1)]
    for req in requests:
        downloader.delay(req, depth=0)  # Start with initial depth
    print(f"Worker {worker_name} completed.")

# Downloader task that fetches HTML content
@app.task
def downloader(url, depth):
    print(f"Downloading {url} at depth {depth}...")
    time.sleep(1)  # Simulate network delay
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        # Pass the HTML content and increase the depth by 1
        scraper.delay(html_content, depth + 1)
        print(f"Downloaded {url}.")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Scraper task that processes the HTML content and extracts data
@app.task
def scraper(html_content, depth):
    print(f"Scraping content at depth {depth}...")
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract data (e.g., page title, headers, links)
    data = {
        "title": soup.title.string if soup.title else "No Title",
        "headers": [header.get_text() for header in soup.find_all(['h1', 'h2', 'h3'])],
        "links": [a['href'] for a in soup.find_all('a', href=True)]
    }
    
    # Save extracted data to a JSON file
    with open(f"scraped_data_depth_{depth}.json", "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"Data scraped at depth {depth}: {data}")

    # Only generate new requests if the max depth has not been reached
    if depth < MAX_DEPTH:
        # Generate a dummy follow-up request (in a real case, this might be other links from the page)
        next_url = "http://localhost:8000/sample_page.html"  # Reuse the local page for simplicity
        downloader.delay(next_url, depth)  # Pass the current depth

    print(f"Scraping completed at depth {depth}.")

