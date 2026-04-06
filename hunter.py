import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from urllib.parse import urlparse, urljoin
import concurrent.futures
import tldextract
import urllib3
import time
import warnings


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def print_banner():
    banner = """
    ==================================================
      🛡️  OMNI-HUNTER v7.6 - BY CYBER TRACE LABS  🛡️
    ==================================================
      Subdomain Recon | Wayback Crawler | Hijack Hunter
    ==================================================
    Developed for: Security Researchers & Bug Hunters
    """
    print(banner)

class OmniHunter:
    def __init__(self, main_domain):
        self.main_domain = main_domain.replace("www.", "").lower()
        self.ext = tldextract.extract(self.main_domain)
        self.root_domain = f"{self.ext.domain}.{self.ext.suffix}"
        
        self.subdomains = set()
        self.all_paths_to_scan = set()
        self.broken_results = []
        self.scanned_links = set() 
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

    def fetch_subdomains(self):
        print(f"[*] Discovering all subdomains for: {self.root_domain}...")
        url = f"https://crt.sh/?q=%.{self.root_domain}&output=json"
        try:
            res = requests.get(url, timeout=25)
            if res.status_code == 200:
                data = res.json()
                for entry in data:
                    sub = entry['name_value'].lower()
                    if "*" not in sub:
                        self.subdomains.add(sub)
                print(f"[+] Found {len(self.subdomains)} subdomains.")
            else:
                self.subdomains.add(self.main_domain)
        except:
            print("[-] Subdomain discovery failed, falling back to main domain.")
            self.subdomains.add(self.main_domain)

    def fetch_archive_paths(self, domain):
        archive_url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=txt&fl=original&collapse=urlkey"
        try:
            res = requests.get(archive_url, timeout=15)
            if res.status_code == 200:
                for line in res.text.splitlines():
                    if line.startswith("http"):
                        self.all_paths_to_scan.add(line)
        except:
            pass

    def check_link_status(self, link, source_page):
        if link in self.scanned_links or self.root_domain in link.lower():
            return 
        if link.startswith(('#', 'javascript:', 'tel:', 'data:')):
            return

        self.scanned_links.add(link)
        try:
            res = requests.head(link, headers=self.headers, timeout=8, allow_redirects=True, verify=False)
            if res.status_code in [403, 405]:
                res = requests.get(link, headers=self.headers, timeout=8, allow_redirects=True, verify=False)

            if res.status_code == 404:
                out = f"[404] {link} | Source: {source_page}"
                print(out)
                self.broken_results.append(out)
        except:
            out = f"[DEAD/HIJACK] {link} | Source: {source_page}"
            print(out)
            self.broken_results.append(out)

    def process_page(self, page_url):
        try:
            res = requests.get(page_url, headers=self.headers, timeout=10, verify=False)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                links = [urljoin(page_url, a['href']) for a in soup.find_all("a", href=True)]
                for l in links:
                    self.check_link_status(l, page_url)
        except:
            pass

    def run(self):
        print_banner()
        start_time = time.time()
        self.fetch_subdomains()
        
        print("[*] Gathering URLs from all subdomains (Wayback Machine)...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            executor.map(self.fetch_archive_paths, list(self.subdomains))
        
        total_paths = len(self.all_paths_to_scan)
        print(f"[+] Total unique pages found to scan: {total_paths}")

        if total_paths == 0:
            print("[-] No paths found. Exiting.")
            return

        print("[*] Starting Stable Scan with 40 threads...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
            executor.map(self.process_page, list(self.all_paths_to_scan))

        self.finish_report(start_time)

    def finish_report(self, start_time):
        filename = f"OMNI_REPORT_{self.root_domain}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"CYBER-TRACE OMNI-HUNTER REPORT: {self.root_domain}\n")
            f.write(f"Total Broken/Dead Links: {len(self.broken_results)}\n")
            f.write("="*60 + "\n\n")
            for result in self.broken_results:
                f.write(result + "\n")
        
        duration = round((time.time() - start_time) / 60, 2)
        print(f"\n[✔] Done! Scan finished in {duration} minutes.")
        print(f"[*] Report saved: {filename}")

if __name__ == "__main__":
    target = input("Enter Target Domain: ").strip()
    OmniHunter(target).run()
