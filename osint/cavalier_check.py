import requests
import json

def check_domain_exposure(domain):
    url = f"https://example.com/api/check?domain={domain}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except json.decoder.JSONDecodeError:
        print("JSON decode error. Response content:")
        print(response.text)
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

