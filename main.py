import argparse
from core.banner import display_banner
from core.connection import check_connection
from core.validation import is_valid_url
from core.scraper import scrape_website
from core.save import save_results
from core.screenshot import take_screenshot
from core.port_scanner import scan_target_ports, quick_scan, stealth_scan, comprehensive_scan, format_scan_results
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
        elif title.upper() == "PORT_SCAN":
            content = format_scan_results(content)
        else:
            content = json.dumps(content, indent=2)
    elif isinstance(content, list):
        if title.upper() == "SUBDOMAINS":
            content = format_subdomains(content)
        else:
            content = "\n".join(f"  • {item}" for item in content)
    
    return f"{color}[{title}]\033[0m\n{content}"

def main():
    parser = argparse.ArgumentParser(description="Advanced OSINT Tool with Enhanced Port Scanning")
    parser.add_argument("--url", required=True, help="Target URL to analyze")
    parser.add_argument("--emails", action="store_true", help="Extract email addresses")
    parser.add_argument("--phones", action="store_true", help="Extract phone numbers")
    parser.add_argument("--links", action="store_true", help="Extract links")
    parser.add_argument("--whois", action="store_true", help="Perform WHOIS lookup")
    parser.add_argument("--ipinfo", action="store_true", help="Get IP geolocation info")
    parser.add_argument("--subdomains", action="store_true", help="Enumerate subdomains")
    parser.add_argument("--check-stealer", action="store_true", help="Check domain exposure")
    parser.add_argument("--screenshot", action="store_true", help="Take website screenshot")
    
    # Enhanced port scanning options
    parser.add_argument("--port-scan", action="store_true", help="Enable port scanning")
    parser.add_argument("--scan-type", choices=['common', 'top1000', 'range', 'quick', 'comprehensive'], 
                       default='common', help="Type of port scan to perform")
    parser.add_argument("--protocol", choices=['tcp', 'udp', 'both'], default='tcp', 
                       help="Protocol to scan (tcp, udp, or both)")
    parser.add_argument("--grab-banner", action="store_true", 
                       help="Grab service banners from open ports")
    parser.add_argument("--stealth", action="store_true", 
                       help="Enable stealth mode for port scanning")
    parser.add_argument("--port-range", nargs=2, type=int, metavar=('START', 'END'),
                       help="Custom port range for scanning (e.g., --port-range 1 1000)")
    
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

    # Screenshot capture with loading animation
    if args.screenshot:
        stop_event = start_loading("Taking website screenshot...")
        results['screenshot'] = take_screenshot(args.url)
        stop_event.set()
        time.sleep(0.1)

    # Port scanning with loading animation
    if getattr(args, 'port_scan', False):
        scan_type = getattr(args, 'scan_type', 'common')
        protocol = getattr(args, 'protocol', 'tcp')
        grab_banner = getattr(args, 'grab_banner', False)
        stealth_mode = getattr(args, 'stealth', False)
        port_range = getattr(args, 'port_range', None)
        
        # Handle custom port range
        if port_range and scan_type == 'range':
            start_port, end_port = port_range
        else:
            start_port, end_port = 1, 1000
        
        if stealth_mode:
            stop_event = start_loading("Performing stealth port scan...")
            results['port_scan'] = stealth_scan(domain, scan_type=scan_type, grab_banner=grab_banner)
        elif scan_type == 'quick':
            stop_event = start_loading("Performing quick port scan...")
            results['port_scan'] = quick_scan(domain, grab_banner=grab_banner)
        elif scan_type == 'comprehensive':
            stop_event = start_loading("Performing comprehensive port scan...")
            results['port_scan'] = comprehensive_scan(domain, grab_banner=grab_banner)
        else:
            stop_event = start_loading(f"Scanning {scan_type} ports...")
            results['port_scan'] = scan_target_ports(
                target=domain,
                scan_type=scan_type,
                start_port=start_port,
                end_port=end_port,
                protocol=protocol,
                grab_banner=grab_banner,
                stealth_mode=stealth_mode
            )
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
