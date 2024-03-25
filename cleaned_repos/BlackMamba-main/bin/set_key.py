"""
Sets the value of cryptography key to a variable.
"""

with open("bin/profile/crypt_key.txt", "r") as f:
    server_key = f.read()
    f.close()
