# Stocktalk

## Purpose
*Stocktalk is a visualization tool that tracks tweet volume and sentiment on Twitter, given a series of queries.*

*It does this by opening a local websocket with Twitter and pulling tweets that contain user-specified keywords. For example, I can tell Stocktalk to grab all tweets that mention Ethereum and periodically tally volume and measure average sentiment every 15 minutes.*

*It will then record this data continuously and update an online database that can be used to visualize the timeseries data via an interactive Flask-based web application.*

## Code Examples
#### Twitter Streaming
> This file opens the websocket and writes to the online databse until manually interrupted
```
/stocktalk
└── listen.py

$ python listen.py
```
```python
from scripts import settings

# Each key or category corresponds to an array of keywords used to pull tweets
queries = {'ETH': ['ETH', 'Ethereum'],
           'LTC': ['LTC', 'Litecoin'],
           'BTC': ['BTC', 'Bitcoin'],
           'XRP': ['XRP', 'Ripple'],
           'XLM': ['XLM', 'Stellar']}

# Aggregate volume and sentiment every 15 minutes
refresh = 15*60

streaming.streamer(settings.credentials, 
                   queries, 
                   refresh, 
                   sentiment=True, 
                   debug=True)
```

#### Realtime Visualization
> This file initiates a local web-application which pulls data from the online database
```
/stocktalk
└── app.py

$ python app.py
```

## Underlying Features
Text Processing

Sentiment Analysis

