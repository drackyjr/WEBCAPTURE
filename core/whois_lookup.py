import whois

def whois_lookup(domain):
    try:
        data = whois.whois(domain)
        return {
            "domain": data.domain_name,
            "registrar": data.registrar,
            "created": str(data.creation_date),
            "expires": str(data.expiration_date),
            "emails": data.emails,
        }
    except Exception as e:
        return {"error": str(e)}
