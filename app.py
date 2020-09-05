from socket import timeout
import requests
import time
from contextlib import suppress
from prometheus_client import start_http_server, REGISTRY, Counter, Gauge

# Remove the default metrics
for name in list(REGISTRY._names_to_collectors.values()):
    with suppress(KeyError):
        REGISTRY.unregister(name)


# Create metrics
SERVICE_UP = Gauge('sample_external_url_up', 'URL Up', ['url'])
SERVICE_LATENCY = Gauge('sample_external_url_response_ms', 'Response Time', ['url'])


# Process the request for a URL
def process_request(url):
    try:
        # Track request start time
        request_time = time.time()
        # Set a timeout of 5 seconds
        # So that the service won't hang if the URL is not responding.
        response = requests.get(url, timeout=5)
        # Calculate the response time
        response_time = time.time() - request_time

        # Check the status code of the response
        if response.status_code == 200:
            SERVICE_UP.labels(url).set(1)
        else:
            # Service is considered as down if the status code is not 200
            SERVICE_UP.labels(url).set(0)

    # Handle timeout
    except requests.exceptions.Timeout:
        # Service is considered as down if timeout
        SERVICE_UP.labels(url).set(0)
        # Set response time to Inf to indicate timeout
        response_time = float('inf')

    SERVICE_LATENCY.labels(url).set(response_time * 1000)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(80)
    # Generate some requests.
    while True:
        urls = ["https://httpstat.us/503", "https://httpstat.us/200"]
        for url in urls:
            process_request(url)