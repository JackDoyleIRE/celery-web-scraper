# main.py
from tasks import add, worker

# Simple task test
add.delay(4, 4)

# Start the worker chain with a specific worker name
worker.delay("Worker_1")