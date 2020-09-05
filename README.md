# Prometheus Metric Monitoring Example
This is a uptime check monitoring service designed to be deployed on Kubernetes Cluster.

This service can be accessed via any endpoint address with HTTP GET request, including `/metrics`, e.g. https://example.com/metrics.

When the endpoint is accessed, this service checks the following two external URLs and return 4 metrics in [Prometheus format](https://prometheus.io/docs/instrumenting/exposition_formats/#text-format-example).
* https://httpstat.us/503
* https://httpstat.us/200

There are two metrics for each URL:
* Whether the URL is up and running
* The response time in milliseconds

A response with 200 status code is considered as up and running, while any other response status code, including 503, are used to indicate the service is down (or attention is needed).

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

See also: [Prometheus](https://prometheus.io/)

## Requirements
This service is developed in Python 3.7. 

The following packages are required:
* requests
* prometheus_client

The exact version of each package is specified in the `requirements.txt` file. To install the package, run:
```
pip install -r requirements.txt
```

## Running the Service
This service can be started by the following command:
```
python app.py
```
By default, the service will check the two URLs every one second.

Optionally, you can specify the time interval between two checks by passing a number with the command:
```
python app.py 5
```
The above command will perform the uptime check every 5 seconds.

## Docker Image
This service is available as a docker image: [qiuosier/prometheus_metrics](https://hub.docker.com/r/qiuosier/prometheus_metrics)

Docker pull command:
```
docker pull qiuosier/prometheus_metrics
```
The docker image is based on `python:3.8-alpine`. Port 80 (HTTP) is exposed for the service.

To run the docker image on local computer, use the following command
```
docker run -dit -p 8080:80 qiuosier/prometheus_metrics
```
This command maps the service to port 8080 on `localhost`. Once the docker image is running, the metrics will be available at http://localhost:8080

The docker image has a default entry point of `python` and default command/argument of `app.py`, which will start the service and perform the uptime check every one second.

See also: [Docker Commands](https://docs.docker.com/engine/reference/commandline/docker/)

## Kubernetes Deployment Specifications
The `deployment.yaml` file contains specifications for deploying this service to a kubernetes cluster using the docker image (`qiuosier/prometheus_metrics`)

The following command will deploy the service on the kubernetes cluster authenticated with your account.
```
kubectl apply -f deployment.yaml
```
See also: [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
