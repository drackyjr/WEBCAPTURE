import re
import requests
from bs4 import BeautifulSoup

def scrape_emails(text):
    pattern = re.compile(r'[\\w\\.-]+@[\\w\\.-]+\\.\\w+')
    return list(set(pattern.findall(text)))

def scrape_phone_numbers(text):
    pattern = re.compile(r'(\\+?\\d{1,3})?[\\s\\-.]?\\(?\\d{2,4}\\)?[\\s\\-.]?\\d{3,5}[\\s\\-.]?\\d{3,5}')
    return list(set(match.group().strip() for match in re.finditer(pattern, text) if len(match.group().strip()) > 6))

def scrape_links(html):
    pattern = re.compile(r'https?://[^\\s"\']+')
    return list(set(pattern.findall(html)))

def scrape_website(url, scrape_em, scrape_ph, scrape_ln):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()
        results = {}
        if scrape_em: results['emails'] = scrape_emails(text)
        if scrape_ph: results['phones'] = scrape_phone_numbers(text)
        if scrape_ln: results['links'] = scrape_links(res.text)
        return results
    except Exception as e:
        return {"error": str(e)}
