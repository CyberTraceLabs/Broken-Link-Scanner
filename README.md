# 🛡️ Omni-Hunter v7.6: Professional Recon & Broken Link Hijacker
**Developed by Cyber Trace Labs**

Omni-Hunter is a high-speed, multi-threaded reconnaissance tool designed for bug bounty hunters and security researchers. It automates the process of subdomain discovery, historical URL extraction from the Wayback Machine, and identifies broken links that are vulnerable to **Domain Hijacking**, **Social Media Takeover**, or **Broken Link Hijacking**.

---

## 🚀 Key Features

* **Subdomain Discovery:** Automatically fetches subdomains using `crt.sh`.
* **Wayback Machine Integration:** Crawls thousands of historical URLs from the Internet Archive to find hidden assets.
* **Stable Multi-Threading:** Optimized with 40 concurrent threads to balance speed and accuracy without triggering rate-limits.
* **Smart Fallback Logic:** Uses both `HEAD` and `GET` requests to minimize False Positives.
* **Comprehensive Reporting:** Generates a detailed `.txt` report with source pages and broken link status.

---

## 🛠️ Installation & Setup

Ensure you have Python 3.10+ installed on your machine.

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/CyberTraceLabs/Broken-Link-Scanner.git](https://github.com/CyberTraceLabs/Broken-Link-Scanner.git)
   cd Broken-Link-Scanner
2.Install Dependencies:
 ```bash
pip install -r requirements.txt

 3.Run the Tool:
   
python hunter.py
 
 
# How it Works:
Phase 1 (Recon): The tool identifies all valid subdomains for the target root domain.

Phase 2 (Crawling): It pulls every recorded URL from the Wayback Machine for each discovered subdomain.

Phase 3 (Hunting): It scans all external links in those pages to find 404 Not Found or DEAD connection errors.

Phase 4 (Reporting): Outputs a final scan report ready for manual verification.

⚠️ Disclaimer
This tool is for educational purposes and authorized security testing only. Cyber Trace Labs is not responsible for any misuse or damage caused by this program.

🤝 Contact
Maintainer: Cyber Trace Labs

Email: cybertracelabs@gmail.com


---
