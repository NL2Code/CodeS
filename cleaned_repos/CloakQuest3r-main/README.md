# CloakQuest3r
CloakQuest3r is a powerful Python tool meticulously crafted to uncover the true IP address of websites safeguarded by Cloudflare and other alternatives, a widely adopted web security and performance enhancement service. Its core mission is to accurately discern the actual IP address of web servers that are concealed behind Cloudflare's protective shield. Subdomain scanning is employed as a key technique in this pursuit. This tool is an invaluable resource for penetration testers, security professionals, and web administrators seeking to perform comprehensive security assessments and identify vulnerabilities that may be obscured by Cloudflare's security measures.

**Key Features:**
- **Real IP Detection:** CloakQuest3r excels in the art of discovering the real IP address of web servers employing Cloudflare's services. This crucial information is paramount for conducting comprehensive penetration tests and ensuring the security of web assets.

- **Subdomain Scanning:** Subdomain scanning is harnessed as a fundamental component in the process of finding the real IP address. It aids in the identification of the actual server responsible for hosting the website and its associated subdomains.

- **IP address History:** Retrieve historical IP address information for a given domain. It uses the ViewDNS service to fetch and display details such as IP address, location, owner, and last seen date.

- **SSL Certificate Analysis:** Extract and analyze SSL certificates associated with the target domain. This could provide additional information about the hosting infrastructure and potentially reveal the true IP address.

- **SecurityTrails API (optional):**  If you add your free SecurityTrails API key to the config.ini file, you can retrieve historical IP information from SecurityTrails.

- **Threaded Scanning:** To enhance efficiency and expedite the real IP detection process, CloakQuest3r utilizes threading. This feature enables the scanning of a substantial list of subdomains without significantly extending the execution time.

- **Detailed Reporting:** The tool provides comprehensive output, including the total number of subdomains scanned, the total number of subdomains found, and the time taken for the scan. Any real IP addresses unveiled during the process are also presented, facilitating in-depth analysis and penetration testing.

With CloakQuest3r, you can confidently evaluate website security, unveil hidden vulnerabilities, and secure your web assets by disclosing the true IP address concealed behind Cloudflare's protective layers.