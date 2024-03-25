## SubDomainizer

SubDomainizer is a tool designed to find hidden subdomains and secrets present is either webpage, Github, and external javascripts present in the given URL.
This tool also finds S3 buckets, cloudfront URL's and more from those JS files which could be interesting like S3 bucket is open to read/write, or subdomain takeover and similar case for cloudfront.
It also scans inside given folder which contains your files.

## Cloud Storage Services Supported:
SubDomainizer can find URL's for following cloud storage services:
```
1. Amazon AWS services (cloudfront and S3 buckets)
2. Digitalocean spaces 
3. Microsoft Azure 
4. Google Cloud Services 
5. Dreamhost 
6. RackCDN. 
```
## Secret Key's Searching: (beta)
SubDomainizer will also find secrets present in content of the page and javascripts files.
Those secret finding depends on some specific keywords and *Shannon Entropy* formula.
It might be possible that some secrets which searched by tool will be false positive.
This secret key searching is in beta and later version might have increased accuracy for search results.
