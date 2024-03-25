# MS-FARMER
A simple bot that uses selenium to farm Microsoft Rewards written in Python
## Launch arguments

- -v/--visible to disable headless
- -l/--lang to force a language (ex: en)
- -g/--geo to force a geolocation (ex: US)
- -p/--proxy to add a proxy to the whole program, supports http/https/socks4/socks5 (overrides per-account proxy in accounts.json) (ex: http://user:pass@host:port)
- -t/--telegram to add a telegram notification, requires Telegram Bot Token and Chat ID (ex: 123456789:ABCdefGhIjKlmNoPQRsTUVwxyZ 123456789)
- -d/--discord to add a discord notification, requires Discord Webhook URL (ex: https://discord.com/api/webhooks/123456789/ABCdefGhIjKlmNoPQRsTUVwxyZ)

## Features

- Bing searches (Desktop, Mobile and Edge) with User-Agents
- Complete automatically the daily set
- Complete automatically punch cards
- Complete automatically the others promotions
- Headless Mode
- Multi-Account Management
- Session storing (3.0)
- 2FA Support (3.0)
- Notifications (discord, telegram) (3.0)
- Proxy Support (3.0)