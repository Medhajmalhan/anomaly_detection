from dash import Dash, dcc, html, no_update
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from stream_simulation import data_stream
from anamoly_detection import IsolationForestDetector
import threading
import numpy as np

# Initialize the Dash app and Isolation Forest Detector
app = Dash(__name__)
detector = IsolationForestDetector(contamination=0.05)  # Set lower contamination
data_x, data_y, anomalies = [], [], []

# Fit initial data with normal values around 10 to establish a baseline
initial_data = [10 + np.random.normal(0, 0.5) for _ in range(100)]  # Steady normal data
detector.fit(initial_data)

# Define the layout for the Dash app
app.layout = html.Div([
    html.H1("Real-Time Data Stream Anomaly Detection (Isolation Forest)"),
    dcc.Graph(id="live-graph"),
    dcc.Interval(id="graph-update", interval=1000, n_intervals=0)  # Update every second
])

# Callback to update the graph at intervals
@app.callback(Output("live-graph", "figure"), [Input("graph-update", "n_intervals")])
def update_graph(n_intervals):
    try:
        global data_x, data_y, anomalies
        new_value = next(stream)  # Get the next data point from the stream

        # Update data and detect anomalies
        data_x.append(n_intervals)
        data_y.append(new_value)
        is_anomaly = detector.detect_anomaly(new_value)  # Detect if the new value is an anomaly
        anomalies.append(new_value if is_anomaly else None)

        # Limit stored data points to avoid memory issues
        MAX_POINTS = 1000
        if len(data_x) > MAX_POINTS:
            data_x = data_x[-MAX_POINTS:]
            data_y = data_y[-MAX_POINTS:]
            anomalies = anomalies[-MAX_POINTS:]

        # Generate the plot
        trace_stream = go.Scatter(x=data_x, y=data_y, mode="lines+markers", name="Data Stream")
        trace_anomaly = go.Scatter(x=data_x, y=anomalies, mode="markers", name="Anomalies", marker=dict(color="red", size=10))
        layout = go.Layout(title="Data Stream with Real-Time Anomaly Detection (Isolation Forest)", xaxis=dict(title="Time"), yaxis=dict(title="Value"))
        
        return {"data": [trace_stream, trace_anomaly], "layout": layout}

    except Exception as e:
        print(f"Error updating graph: {e}")
        return no_update

# Run the data stream in a separate thread to avoid blocking
def start_stream():
    global stream
    stream = data_stream()

stream_thread = threading.Thread(target=start_stream)
stream_thread.start()

if __name__ == "__main__":
    app.run_server(debug=True)
