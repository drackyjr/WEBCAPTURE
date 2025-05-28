import requests
import sys
from .banner import Colors

def check_connection():
    print(f"{Colors.BrightWhite}[{Colors.BrightRed}!{Colors.BrightWhite}] {Colors.BrightRed}Checking internet...{Colors.Reset}")
    try:
        requests.get("http://google.com", timeout=5)
        print(f"{Colors.BrightWhite}[{Colors.BrightYellow}*{Colors.BrightWhite}] {Colors.BrightYellow}Connected.{Colors.Reset}")
    except requests.ConnectionError:
        print(f"{Colors.BrightRed}[!] No internet.{Colors.Reset}")
        sys.exit(1)
