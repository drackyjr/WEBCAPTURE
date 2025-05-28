import requests

def check_domain_exposure(domain):
    url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-domain?domain={domain}"
    return requests.get(url).json()
