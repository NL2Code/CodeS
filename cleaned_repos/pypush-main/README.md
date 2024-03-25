# pypush

`pypush` is a POC demo of my recent iMessage reverse-engineering.
It can currently register as a new device on an Apple ID, set up encryption keys, and ***send and receive iMessages***!

`pypush` is completely platform-independent, and does not require a Mac or other Apple device to use!

## Operation
`pypush` will generate a `config.json` in the repository when you run demo.py. DO NOT SHARE THIS FILE.
It contains all the encryption keys necessary to log into you Apple ID and send iMessages as you.

Once it loads, it should prompt you with `>>`. Type `help` and press enter for a list of supported commands.
