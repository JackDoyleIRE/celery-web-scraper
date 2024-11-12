from celery import Celery
import time

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y

# Worker task that initiates the download and scrape process
@app.task
def worker(worker_name: str):
    print(f"Worker {worker_name} started.")
    # Simulate some requests
    requests = [f"request_{i}" for i in range(5)]
    for req in requests:
        downloader.delay(req)  # Initiate downloader task for each request
    print(f"Worker {worker_name} completed.")

# Downloader task that simulates downloading data
@app.task
def downloader(request):
    print(f"Downloading {request}...")
    time.sleep(1)  # Simulate network delay
    response = f"response for {request}"
    scraper.delay(response)  # Pass the response to the scraper task
    print(f"Downloaded {request}.")

# Scraper task that processes the downloaded data
@app.task
def scraper(response):
    print(f"Scraping {response}...")
    scraps = [f"scrap_data_{i}" for i in range(2)]
    requests = [f"new_request_{i}" for i in range(2)]
    for scrap in scraps:
        print(f"Saving {scrap} to database (mock).")
    for req in requests:
        downloader.delay(req)  # Send new requests to the downloader
    print(f"Scraping completed for {response}.")