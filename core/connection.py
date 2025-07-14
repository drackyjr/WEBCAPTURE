import requests
import sys
from .banner import Colors

# This function checks if the system has an active internet connection
def check_connection():
    print(f"{Colors.BrightWhite}[{Colors.BrightRed}!{Colors.BrightWhite}] {Colors.BrightRed}Checking internet...{Colors.Reset}")

    try:
        # Try to connect to Google with a short timeout
        requests.get("http://google.com", timeout=5)
        print(f"{Colors.BrightWhite}[{Colors.BrightYellow}*{Colors.BrightWhite}] {Colors.BrightYellow}Connected.{Colors.Reset}")

    except requests.ConnectionError:
        # If it fails, print an error and exit the script
        print(f"{Colors.BrightRed}[!] No internet.{Colors.Reset}")
        sys.exit(1)

