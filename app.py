import requests
import time
import argparse
from contextlib import suppress
from prometheus_client import start_http_server, REGISTRY, Gauge

# Remove the default metrics
for name in list(REGISTRY._names_to_collectors.values()):
    with suppress(KeyError):
        REGISTRY.unregister(name)


# Create metrics
SERVICE_UP = Gauge('sample_external_url_up', 'URL Up', ['url'])
SERVICE_LATENCY = Gauge('sample_external_url_response_ms', 'Response Time', ['url'])


# Process the request for a URL
def check_url(url):
    """Checks if a URL is up and track the response time by sending HTTP GET request.

    Args:
        url (str): The URL to be checked.

    Returns: None
    """
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
    
    # Save response time in milliseconds
    SERVICE_LATENCY.labels(url).set(response_time * 1000)


def uptime_check(delay=1):
    """Performs uptime checks to two URLs

    Args: 
        delay: The number of seconds delay between two uptime checks, optional, defaults to 1 second.

    Returns: None
    """
    urls = ["https://httpstat.us/503", "https://httpstat.us/200"]
    for url in urls:
        check_url(url)
        time.sleep(delay)


def parse_arguments():
    """Parses the command line arguments.
    This service takes one optional argument, 
    which is the number of seconds delay between each uptime check.
    Each uptime check sends requests to two URLs.

    Returns:
        int: Number of seconds
    """
    parser = argparse.ArgumentParser(description="Uptime check service arguments.")
    parser.add_argument('delay', type=int, nargs='?', help="Time interval between two uptime checks in seconds.")
    args = parser.parse_args()
    if args.delay:
        return args.delay
    return 1


# This is the main function
# This following lines are not tested due to the infinite loop
if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(80)
    # Generate some requests.
    while True:
        uptime_check(parse_arguments())
