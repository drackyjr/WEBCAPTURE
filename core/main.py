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
        print("Invalid URL.")
        return

    domain = args.url.split("//")[-1].split("/")[0]

    results = scrape_website(args.url, args.emails, args.phones, args.links)
    if args.whois: results['whois'] = whois_lookup(domain)
    if args.ipinfo: results['ipinfo'] = ip_info(domain)
    if args.subdomains: results['subdomains'] = enumerate_subdomains(domain)
    if args.check_stealer: results['cavalier'] = check_domain_exposure(domain)

    for k, v in results.items():
        print(f"\\n[{k.upper()}]")
        print(v)

    if args.save:
        save_results(results, args.save)

if __name__ == "__main__":
    main()
