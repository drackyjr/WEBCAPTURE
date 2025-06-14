import socket
import requests

def ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        geo = requests.get(f"https://ipinfo.io/{ip}/json").json()
        return {"ip": ip, **geo}
    except Exception as e:
        return {"error": str(e)}
