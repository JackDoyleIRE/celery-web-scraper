from celery_app import app
import time

@app.task
def worker(worker_name: str):
    print(f"Worker {worker_name} started.")
    # Fake requests for simplicity
    requests = [f"request_{i}" for i in range(5)]
    for req in requests:
        downloader.delay(req)
    print(f"Worker {worker_name} completed.")

@app.task
def downloader(request):
    print(f"Downloading {request}...")
    time.sleep(1)  # Simulating network delay
    response = f"response for {request}"
    scraper.delay(response)
    print(f"Downloaded {request}.")

@app.task
def scraper(response):
    print(f"Scraping {response}...")
    scraps = [f"scrap_data_{i}" for i in range(2)]
    requests = [f"new_request_{i}" for i in range(2)]
    for scrap in scraps:
        print(f"Saving {scrap} to database (mock).")
    for req in requests:
        downloader.delay(req)
    print(f"Scraping completed for {response}.")
