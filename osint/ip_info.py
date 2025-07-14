import socket
import requests

# This function gets the IP address of a domain and gathers info about it
def ip_info(domain):
    try:
        # First, get the IP address of the domain
        ip = socket.gethostbyname(domain)

        # Then, ask ipinfo.io for more details about that IP
        geo = requests.get(f"https://ipinfo.io/{ip}/json").json()

        # Combine the IP address with the data from ipinfo
        return {"ip": ip, **geo}

    except Exception as e:
        # If anything fails, return the error as a message
        return {"error": str(e)}


