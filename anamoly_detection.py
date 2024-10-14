from sklearn.ensemble import IsolationForest
import numpy as np

class IsolationForestDetector:
    def __init__(self, contamination=0.05, max_samples=100):
        """Initialize with lower contamination for fewer anomalies."""
        self.model = IsolationForest(contamination=contamination, max_samples=max_samples)
        self.data_buffer = []

    def fit(self, initial_data):
        """Fit the model on initial data to establish a baseline."""
        self.data_buffer.extend(initial_data)
        self.model.fit(np.array(self.data_buffer).reshape(-1, 1))

    def detect_anomaly(self, new_value):
        """Predict if a new value is an anomaly."""
        self.data_buffer.append(new_value)
        if len(self.data_buffer) > 100:
            self.data_buffer.pop(0)  # Maintain a sliding window

        prediction = self.model.predict(np.array([new_value]).reshape(-1, 1))
        is_anomaly = prediction[0] == -1
        if is_anomaly:
            print(f"Detected Anomaly: {new_value}")  # Log detected anomalies
        return is_anomaly
