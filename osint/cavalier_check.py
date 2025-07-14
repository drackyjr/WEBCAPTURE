import requests
import json

# This function checks if the given domain has been exposed in any way
def check_domain_exposure(domain):
    # Build the URL to send the request to
    url = f"https://example.com/api/check?domain={domain}"

    try:
        # Send a GET request to the API
        response = requests.get(url)

        # Raise an error if the response status is 4xx or 5xx
        response.raise_for_status()

        # Try to parse the response as JSON and return it
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # If there was an HTTP error, print the error message
        print(f"HTTP error occurred: {http_err}")

    except json.decoder.JSONDecodeError:
        # If the response isn't valid JSON, print the raw text
        print("JSON decode error. Response content:")
        print(response.text)

    except Exception as err:
        # Catch all other errors and print them
        print(f"An error occurred: {err}")

    # If anything failed, return None
    return None

