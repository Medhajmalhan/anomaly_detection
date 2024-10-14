import numpy as np
import random
import time

def data_stream():
    """Generates a simulated data stream with seasonal patterns and distinct anomalies."""
    counter = 0
    while True:
        # Seasonal pattern
        normal_value = 10 + np.sin(counter / 10) + np.random.normal(0, 0.5)  # Adding seasonal variation
        anomaly = 100 if counter % random.randint(10, 15) == 0 else 0  # Anomaly every 10-15 points
        yield normal_value + anomaly
        counter += 1
        time.sleep(0.1)
