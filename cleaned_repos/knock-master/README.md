# Knock Subdomain Scan v6.1.0

Knockpy is a portable and modular python3 tool designed to quickly enumerate subdomains on a target domain through **passive reconnaissance** and **dictionary scan**.

### Very simply
```bash
python3 knockpy.py domain.com
```
---

### Full scan
```bash
$ knockpy domain.com
```

- Scan type: **dns** + **http(s)** requests
- Wordlist: **local** + **remote**

Knockpy uses by default a internal file **wordlist.txt** and a remote list obtained by scanning other sources (passive recon) through **plugins**. To use a custom dictionary you can use the ```-w``` option and specify the path to your local dictionary. Also, you can write a new plugin to populate the wordlist with subdomains obtained from external services. Take a look at the ones in the [remote](knockpy/remote) folder and use them as an example. Remember that some plugins, like [Virustotal](knockpy/remote/api_virustotal.py) or [Shodan](knockpy/remote/api_shodan.py), need apikey to work.

The domain target can be passed via STDIN.

```bash
echo "domain.com" | knockpy
```

To ignore http(s) responses with specific code, you can use the ```--no-http-code``` followed by the code list ```404 500 530```. With the ```--no-ip``` option you can ignore ip list ```192.168.1.100 192.168.101 192.168.1.102```
