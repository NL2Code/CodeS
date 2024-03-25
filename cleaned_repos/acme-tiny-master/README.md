# acme-tiny

This is a tiny, auditable script that you can throw on your server to issue
and renew [Let's Encrypt](https://letsencrypt.org/) certificates. Since it has
to be run on your server and have access to your private Let's Encrypt account
key, I tried to make it as tiny as possible (currently less than 200 lines).
The only prerequisites are python and openssl.

## How to use this script

If you already have a Let's Encrypt issued certificate and just want to renew,
you should only have to do Steps 3 and 6.

- Step 1: Create a Let's Encrypt account private key (if you haven't already)

- Step 2: Create a certificate signing request (CSR) for your domains.

- Step 3: Make your website host challenge files

- Step 4: Get a signed certificate!

- Step 5: Install the certificate

- Step 6: Setup an auto-renew cronjob