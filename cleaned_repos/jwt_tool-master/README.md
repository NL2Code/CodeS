# The JSON Web Token Toolkit v2
>*jwt_tool.py* is a toolkit for validating, forging, scanning and tampering JWTs (JSON Web Tokens).  

Its functionality includes:
* Checking the validity of a token
* Testing for known exploits:
  * (CVE-2015-2951) The ***alg=none*** signature-bypass vulnerability
  * (CVE-2016-10555) The ***RS/HS256*** public key mismatch vulnerability
  * (CVE-2018-0114) ***Key injection*** vulnerability
  * (CVE-2019-20933/CVE-2020-28637) ***Blank password*** vulnerability
  * (CVE-2020-28042) ***Null signature*** vulnerability
* Scanning for misconfigurations or known weaknesses
* Fuzzing claim values to provoke unexpected behaviours
* Testing the validity of a secret/key file/Public Key/JWKS key
* Identifying ***weak keys*** via a High-speed ***Dictionary Attack***
* Forging new token header and payload contents and creating a new signature with the **key** or via another attack method
* Timestamp tampering
* RSA and ECDSA key generation, and reconstruction (from JWKS files)
* ...and lots more!