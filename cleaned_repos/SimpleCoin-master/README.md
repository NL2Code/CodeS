# SimpleCoin

Just a really simple, insecure and incomplete implementation of a blockchain for a cryptocurrency made in Python. The goal of this project is to make a working blockchain currency, keeping it as simple as possible and to be used as educational material.

## What is a blockchain?

Taking a look at the Bitcoin organization wiki website we can find this definition:

>A block chain is a transaction database shared by all nodes participating in a system based on the Bitcoin protocol. A full copy of a currency's block chain contains every transaction ever executed in the currency. With this information, one can find out how much value belonged to each address at any point in history.

In simpler terms, blockchain can be seen as a distributed ledger recording each transaction in the network. Each transaction is identified by the public key of the block which is a hash function of the private key. The distributed ledger makes data manipulation in the blockchain difficult, nearly impossible. 


## How this code work?

There are 2 main scripts:

- ```miner.py```
- ```wallet.py```

### Miner.py

This file is probably the most important. Running it will create a node (like a server). From here you can connect to the blockchain and process transactions (that other users send) by mining. As a reward for this work, you recieve some coins. The more nodes exist, the more secure the blockchain gets.

```miner.py``` has 2 processes running in parallel:

1. The first process takes care of mining, updating new blockchains and finding the proof of work.

2. The second process runs the flask server where peer nodes and users can connect to ask for the entire blockchain or submit new transactions.

> Parallel processes don't run in python IDLE, so make sure you are running it from the console.

The following flowchart provides a simple , high-level understanding of what the miner does


### Wallet.py

This file is for those who don't want to be nodes but simple users. Running this file allows you to generate a new address, send coins and check your transaction history (keep in mind that if you are running this in a local server, you will need a "miner" to process your transaction).
When creating a wallet address, a new file will be generated with all your security credentials. You are supposed to keep it safe.

