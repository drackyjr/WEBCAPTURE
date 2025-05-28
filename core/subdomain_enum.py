import requests

def enumerate_subdomains(domain):
    try:
        res = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=10)
        entries = res.json()
        subs = set()
        for e in entries:
            for s in e['name_value'].split('\\n'):
                if domain in s:
                    subs.add(s.strip())
        return list(subs)
    except Exception as e:
        return {"error": str(e)}
