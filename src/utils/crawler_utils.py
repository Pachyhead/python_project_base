import random
import time

def human_like_interval(min_sec: float = 1.0, max_sec: float = 3.0):
    # Wait for a random time between min and max seconds
    wait_time = random.uniform(min_sec, max_sec)
    time.sleep(wait_time)