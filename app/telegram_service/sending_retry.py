import requests  # type: ignore


def send_telegram_request(url: str, payload: dict) -> str:
    """
    Sends a request to the Telegram API endpoint with retry logic.
    Retries up to 3 times on failure.

    Returns a formatted response string for logging directly.
    """

    max_retries = 3
    attempt = 0

    while True:
        attempt += 1
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            return f"tg response: {response.status_code}, Success: {response.ok}..."
        except Exception as e:
            if attempt >= max_retries - 1:
                return f"failed to send to tg: {e}"
            continue
