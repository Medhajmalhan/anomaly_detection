# Efficient Data Stream Anomaly Detection

This project implements a real-time anomaly detection system for streaming data, utilizing Z-score thresholding and a sliding window. The project includes real-time data simulation, anomaly detection, and visualization using Dash.

## How to Run

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python main.py`
3. View the real-time dashboard in your web browser at `http://127.0.0.1:8050`.

## Key Components

- **Data Stream Simulation**: Generates data with seasonality, noise, and random anomalies.
- **Anomaly Detection**: Flags anomalies based on a Z-score threshold.
- **Real-Time Visualization**: Displays data and detected anomalies on an interactive dashboard.
