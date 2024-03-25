# What's Arjun?

Arjun can find query parameters for URL endpoints. If you don't get what that means, it's okay, read along.

Web applications use parameters (or queries) to accept user input, take the following example into consideration

`http://api.example.com/v1/userinfo?id=751634589`

This URL seems to load user information for a specific user id, but what if there exists a parameter named `admin` which when set to `True` makes the endpoint provide more information about the user?\
This is what Arjun does, it finds valid HTTP parameters with a huge default dictionary of 25,890 parameter names.

The best part? It takes less than 10 seconds to go through this huge list while making just 50-60 requests to the target. [Here's how](https://github.com/s0md3v/Arjun/wiki/How-Arjun-works%3F).

### Why Arjun?

- Supports `GET/POST/POST-JSON/POST-XML` requests
- Automatically handles rate limits and timeouts
- Export results to: BurpSuite, text or JSON file
- Import targets from: BurpSuite, text file or a raw request file
- Can passively extract parameters from JS or 3 external sources