# Striker

### Workflow
##### Phase 1: Attack Surface Discovery
This phase includes finding subdomains of the user specified domain, filtering alive hosts as well scanning of 1000 most common TCP ports.
##### Phase 2: Sweeping
Mass scanning of misconfigured HTTP response headers, croassdomain.xml as well as checks for some sensitive files is done in this phase.
##### Phase 3: Agressive Information Gathering
This phase is dedicated to data gathering by crawling the subdomains. The gathered data is used to find outdated JS libraries, detect CMS and technologies in use.\
HTML forms that are tested in later phases for vulnerability detection are also collected during this crawling.
##### Phase 4: Vulnerability Scanning
This phase is under development