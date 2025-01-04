
It's very convenient to download the cryptocurrency data with [binance-public-data](https://github.com/binance/binance-public-data) project.

1. Clone the github

```
$ git clone https://github.com/binance/binance-public-data.git
```

2. Install the dependencies

```
$ cd binance-public-data
$ pip install -r requirements.txt
```

3. Download the data

```
$ export STORE_DIRECTORY=<your desired path> 
$ python python/download-kline.py -t spot -s ETHUSDT BTCUSDT BNBBUSD -startDate 2017-06-01
```