
# Website Uptime Monitor

A simple Python and Streamlit dashboard for checking website availability
and measuring response times.

## Features

- Check a website using its URL
- Display HTTP status and response time
- Calculate uptime from recorded checks
- View response-time charts and check history
- Run the application using Docker
- Test the monitoring logic using pytest
- Automate testing with GitHub Actions
- Deploy using Kubernetes

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Run with Docker

```bash
docker build -t website-monitor .
docker run --rm -p 8080:8501 website-monitor
```

Open http://localhost:8080.

## Run tests

```bash
python -m pytest
```

## Kubernetes

Apply the manifests after building the image and setting up a
Kubernetes cluster:

```bash
kubectl apply -f k8s/
kubectl get pods
```
