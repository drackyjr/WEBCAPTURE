import re
import requests
from bs4 import BeautifulSoup

# Extracts all unique email addresses from the text
def scrape_emails(text):
    pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
    return list(set(pattern.findall(text)))

# Extracts phone numbers from the text using a basic international pattern
def scrape_phone_numbers(text):
    pattern = re.compile(r'(\+?\d{1,3})?[\s\-.]?\(?\d{2,4}\)?[\s\-.]?\d{3,5}[\s\-.]?\d{3,5}')
    return list(set(
        match.group().strip()
        for match in re.finditer(pattern, text)
        if len(match.group().strip()) > 6  # Filter out very short invalid matches
    ))

# Extracts all valid HTTP and HTTPS links from the HTML
def scrape_links(html):
    pattern = re.compile(r'https?://[^\s"\'<>]+')
    return list(set(pattern.findall(html)))

# Scrapes the target URL for emails, phone numbers, and links based on flags
def scrape_website(url, scrape_em, scrape_ph, scrape_ln):
    try:
        # Send a request with a common User-Agent header to avoid blocks
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        res.raise_for_status()  # Raise error if the response isn't 200 OK

        # Parse the HTML using BeautifulSoup and extract visible text
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()

        results = {}

        # Run extractors based on user input
        if scrape_em:
            results['emails'] = scrape_emails(text)

        if scrape_ph:
            results['phones'] = scrape_phone_numbers(text)

        if scrape_ln:
            results['links'] = scrape_links(res.text)

        return results

    except Exception as e:
        # Return error message in case of failure
        return {"error": str(e)}

