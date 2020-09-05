# Prometheus Metric Monitoring Example
This is a uptime check monitoring service designed to be deployed on Kubernetes Cluster.

This service can be accessed via `/metrics` endpoint with HTTP GET request, e.g. https://example.com/metrics.

When the endpoint is accessed, this service checks the following two external URLs and return 4 metrics in [Prometheus format](https://prometheus.io/docs/instrumenting/exposition_formats/#text-format-example).
* https://httpstat.us/503
* https://httpstat.us/200

There are two metrics for each URL:
* Whether the URL is up and running
* The response time in milliseconds

A response with 200 status code is considered as up and running, while a response with 503 status code indicates the service is down.

Below is an example of the response:
```
# HELP sample_external_url_up URL Up
# TYPE sample_external_url_up gauge
sample_external_url_up{url="https://httpstat.us/503"} 0.0
sample_external_url_up{url="https://httpstat.us/200"} 1.0
# HELP sample_external_url_response_ms Response Time
# TYPE sample_external_url_response_ms gauge
sample_external_url_response_ms{url="https://httpstat.us/503"} 298.56300354003906
sample_external_url_response_ms{url="https://httpstat.us/200"} 306.61916732788086
```

This service is developed in Python 3.7.