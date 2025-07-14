import whois

# This function looks up WHOIS info for a domain
def whois_lookup(domain):
    try:
        # Use the whois module to get details about the domain
        data = whois.whois(domain)

        # Extract and return only the useful parts
        return {
            "domain": data.domain_name,
            "registrar": data.registrar,
            "created": str(data.creation_date),
            "expires": str(data.expiration_date),
            "emails": data.emails,
        }

    except Exception as e:
        # If the lookup fails (invalid domain, no record, etc), return the error
        return {"error": str(e)}

