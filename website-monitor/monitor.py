
import time
from urllib.parse import urlparse

import requests


def check_website(url, timeout=5):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return {
            "status": "DOWN",
            "status_code": 0,
            "latency_ms": None,
            "error": "Enter a valid HTTP or HTTPS URL.",
        }

    start = time.perf_counter()

    try:
        response = requests.get(url, timeout=timeout)
        latency = round((time.perf_counter() - start) * 1000, 2)

        return {
            "status": "UP" if response.status_code < 500 else "DOWN",
            "status_code": response.status_code,
            "latency_ms": latency,
            "error": None,
        }

    except requests.RequestException:
        return {
            "status": "DOWN",
            "status_code": 0,
            "latency_ms": None,
            "error": "Website could not be reached.",
        }
