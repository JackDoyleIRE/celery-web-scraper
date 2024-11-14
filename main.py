# main.py
from tasks import worker

# Start the worker chain with a specific worker name
worker.delay("Worker_1")