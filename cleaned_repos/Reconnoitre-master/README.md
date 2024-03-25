# Reconnoitre
A reconnaissance tool made for the OSCP labs to automate information gathering and service enumeration whilst creating a directory structure to store  results, findings and exploits used for each host, recommended commands to execute and directory structures for storing loot and flags.

# Usage

This tool can be used and copied for personal use freely however attribution and credit should be offered to Mike Czumak who originally started the process of automating this work.

| Argument        | Description |
| ------------- |:-------------|
| -h, --help | Display help message and exit |
| -t TARGET_HOSTS | Set either a target range of addresses or a single host to target. May also be a file containing hosts. |
| -o OUTPUT_DIRECTORY | Set the target directory where results should be written. |
| -w WORDLIST | Optionally specify your own wordlist to use for pre-compiled commands, or executed attacks. |
| --pingsweep | Write a new target.txt file in the OUTPUT_DIRECTORY by performing a ping sweep and discovering live hosts. |
| --dns, --dnssweep | Find DNS servers from the list of target(s). |
| --snmp | Find hosts responding to SNMP requests from the list of target(s). |
| --services | Perform a service scan over the target(s) and write recommendations for further commands to execute. |
| --hostnames | Attempt to discover target hostnames and write to hostnames.txt. |
| --virtualhosts | Attempt to discover virtual hosts using the specified wordlist. This can be expended via discovered hostnames. |
| --ignore-http-codes | Comma separated list of http codes to ignore with virtual host scans. |
| --ignore-content-length | Ignore content lengths of specificed amount. This may become useful when a server returns a static page on every virtual host guess. |
| --quiet | Supress banner and headers and limit feedback to grepable results. |
| --quick | Move to the next target after performing a quick scan and writing first-round recommendations. |
| --no-udp | Disable UDP service scanning, which is ON by default. |