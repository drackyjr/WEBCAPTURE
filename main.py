import argparse
from core.banner import display_banner
from core.connection import check_connection
from core.validation import is_valid_url
from core.scraper import scrape_website
from core.save import save_results
from osint.whois_lookup import whois_lookup
from osint.ip_info import ip_info
from osint.subdomain_enum import enumerate_subdomains
from osint.cavalier_check import check_domain_exposure
import json
from datetime import datetime
import sys
import time
import threading
from core.banner import Colors

def loading_animation(stop_event, message):
    """Display a loading animation while processing"""
    animation = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Colors.BrightCyan}{animation[idx % len(animation)]} {message}{Colors.Reset}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")  # Clear the loading animation

def start_loading(message):
    """Start the loading animation in a separate thread"""
    stop_event = threading.Event()
    thread = threading.Thread(target=loading_animation, args=(stop_event, message))
    thread.daemon = True
    thread.start()
    return stop_event

def format_whois(whois_data):
    if not whois_data:
        return "No WHOIS data available"
    
    formatted = []
    for key, value in whois_data.items():
        if isinstance(value, list):
            value = "\n    " + "\n    ".join(value)
        formatted.append(f"{key}: {value}")
    return "\n".join(formatted)

def format_ipinfo(ipinfo_data):
    if not ipinfo_data:
        return "No IP information available"
    
    formatted = []
    for key, value in ipinfo_data.items():
        if key != 'readme':
            formatted.append(f"{key}: {value}")
    return "\n".join(formatted)

def format_subdomains(subdomains):
    if not subdomains:
        return "No subdomains found"
    
    # Remove duplicates and sort
    unique_subdomains = sorted(set(subdomains))
    return "\n".join(f"  • {subdomain}" for subdomain in unique_subdomains)

def format_section(title, content, color="\033[1;97m"):
    if not content:
        return f"{color}[{title}]\033[0m\nNo data available"
    
    if isinstance(content, dict):
        if title.upper() == "WHOIS":
            content = format_whois(content)
        elif title.upper() == "IPINFO":
            content = format_ipinfo(content)
        else:
            content = json.dumps(content, indent=2)
    elif isinstance(content, list):
        if title.upper() == "SUBDOMAINS":
            content = format_subdomains(content)
        else:
            content = "\n".join(f"  • {item}" for item in content)
    
    return f"{color}[{title}]\033[0m\n{content}"

def main():
    parser = argparse.ArgumentParser(description="Advanced OSINT Tool")
    parser.add_argument("--url", required=True)
    parser.add_argument("--emails", action="store_true")
    parser.add_argument("--phones", action="store_true")
    parser.add_argument("--links", action="store_true")
    parser.add_argument("--whois", action="store_true")
    parser.add_argument("--ipinfo", action="store_true")
    parser.add_argument("--subdomains", action="store_true")
    parser.add_argument("--check-stealer", action="store_true")
    parser.add_argument("--save", type=str, help="Folder to save results")
    args = parser.parse_args()

    display_banner()
    check_connection()

    if not is_valid_url(args.url):
        print("\033[1;91m[ERROR] Invalid URL.\033[0m")
        return

    domain = args.url.split("//")[-1].split("/")[0]
    print(f"\n{Colors.BrightCyan}[*] Scanning domain: {domain}{Colors.Reset}\n")

    # Start loading animation for website scraping
    stop_event = start_loading("Scraping website...")
    results = scrape_website(args.url, args.emails, args.phones, args.links)
    stop_event.set()
    time.sleep(0.1)  # Small delay to ensure animation is cleared

    # WHOIS lookup with loading animation
    if args.whois:
        stop_event = start_loading("Performing WHOIS lookup...")
        results['whois'] = whois_lookup(domain)
        stop_event.set()
        time.sleep(0.1)

    # IP info with loading animation
    if args.ipinfo:
        stop_event = start_loading("Gathering IP information...")
        results['ipinfo'] = ip_info(domain)
        stop_event.set()
        time.sleep(0.1)

    # Subdomain enumeration with loading animation
    if args.subdomains:
        stop_event = start_loading("Enumerating subdomains...")
        results['subdomains'] = enumerate_subdomains(domain)
        stop_event.set()
        time.sleep(0.1)

    # Cavalier check with loading animation
    if args.check_stealer:
        stop_event = start_loading("Checking domain exposure...")
        results['cavalier'] = check_domain_exposure(domain)
        stop_event.set()
        time.sleep(0.1)

    # Define colors for different sections
    colors = {
        'WHOIS': '\033[1;92m',  # Green
        'IPINFO': '\033[1;94m',  # Blue
        'SUBDOMAINS': '\033[1;95m',  # Magenta
        'CAVALIER': '\033[1;93m',  # Yellow
        'ERROR': '\033[1;91m',  # Red
    }

    print(f"\n{Colors.BrightGreen}[+] Scan completed!{Colors.Reset}\n")
    print(f"{Colors.BrightGreen}─" * 80 + Colors.Reset)

    for k, v in results.items():
        color = colors.get(k.upper(), '\033[1;97m')  # Default to white
        print(format_section(k.upper(), v, color))
        print("\n" + "─" * 80 + "\n")  # Add separator

    if args.save:
        stop_event = start_loading("Saving results...")
        save_results(results, args.save)
        stop_event.set()
        time.sleep(0.1)
        print(f"\n{Colors.BrightGreen}[+] Results saved to {args.save}{Colors.Reset}")

if __name__ == "__main__":
    main()
