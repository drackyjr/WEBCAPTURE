import requests

# This function finds subdomains for a given domain using crt.sh (Certificate Transparency logs)
def enumerate_subdomains(domain):
    try:
        # Send a request to crt.sh to look for any certificates related to subdomains
        res = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=10)

        # Convert the JSON response into a Python list of entries
        entries = res.json()

        # We'll collect all the subdomains here (using a set to avoid duplicates)
        subs = set()

        # Go through each entry, and split by newline if there are multiple names in one field
        for e in entries:
            for s in e['name_value'].split('\\n'):
                if domain in s:
                    subs.add(s.strip())  # Clean up any extra spaces

        # Convert the set into a list before returning
        return list(subs)

    except Exception as e:
        # If anything fails (like timeout, bad response, etc), return the error
        return {"error": str(e)}

