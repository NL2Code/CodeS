# Merged Into MassBrowser
MassBrowser is a state-of-the-art system designed to circumvent Internet censorship. MassBrowser is open-source and free-to-use. It has been designed and developed by the Secure, Private Internet (SPIN) Research Group at the University of Massachusetts Amherst. MassBrowser operates with the help of normal Internet users with open access to the Internet who volunteer to help censored Internet users.

Know your privacy guarantees: Using MassBrowser you will have the same level of privacy as using public VPNs or public HTTPS proxies. Therefore, the volunteer who is proxying your traffic will know your IP address as well as the websites you are browsing. For HTTPS websites (e.g., any URL starting with "https://"), the volunteer proxy will not be able to see your passwords or other data that you exchange with those websites. This is not true for HTTP websites. Therefore, use MassBrowser as a replacement for public VPNs and HTTPS proxies. If you plan to do something sensitive on the Internet that makes you worried about your anonymity, use a software like Tor (your connections will be much slower on Tor) or tunnel Tor over MassBrowser.

Know the security of your local certificate: During installation, MassBrowser asks you to install a local certificate in your Firefox browser. This local certificate is required for MassBrowser to implement an essential optimization technique called CDNBrowsing (which is described in the geek's section). Note that the certificate is locally created in your browser, is unique for each client, and never leaves your computer. Therefore no one, not even us, will be able to use that local certificate to eavesdrop your traffic. Make sure you do not share this local certificate with others. You can simply remove the certificate at any time by going to your Firefox settings.

## Example
```
cachebrowser bootstrap www.nbc.com
cachebrowser get http://www.nbc.com

cachebrowser get https://www.istockphoto.com 69.31.76.91
```

