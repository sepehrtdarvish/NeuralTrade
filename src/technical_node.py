import requests

class TechnicalMiner:
    def __init__(self, symbol="BTCUSDT"):
        self.symbol = symbol
        # Bybit API for Price Data
        self.bybit_url = "https://api.bybit.com/v5/market"
        # Alternative.me API for Fear & Greed Index
        self.fng_url = "https://api.alternative.me/fng/"

    def get_fear_and_greed(self):
        """
        Fetch the latest Fear and Greed Index value.
        0 = Extreme Fear, 100 = Extreme Greed.
        """
        try:
            response = requests.get(self.fng_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            fng_value = data['data'][0]['value']
            fng_classification = data['data'][0]['value_classification']
            return {
                "fng_score": int(fng_value),
                "fng_label": fng_classification
            }
        except Exception as e:
            print(f"Error fetching Fear & Greed Index: {e}")
            return None

    def get_market_data(self):
        """
        Fetch comprehensive market data including Price, Volume, and Sentiment.
        """
        try:
            # 1. Fetch Price Ticker Data
            ticker_url = f"{self.bybit_url}/tickers?category=spot&symbol={self.symbol}"
            ticker_response = requests.get(ticker_url, timeout=10)
            ticker_response.raise_for_status()
            ticker_data = ticker_response.json()['result']['list'][0]

            # 2. Fetch Daily Klines (Candles) for 7-day change
            kline_url = f"{self.bybit_url}/kline?category=spot&symbol={self.symbol}&interval=D&limit=8"
            kline_response = requests.get(kline_url, timeout=10)
            kline_response.raise_for_status()
            klines_data = kline_response.json()['result']['list']
            
            current_price = float(ticker_data['lastPrice'])
            price_7d_ago = float(klines_data[-1][4]) 
            price_change_7d = ((current_price - price_7d_ago) / price_7d_ago) * 100
            price_change_24h = float(ticker_data.get('price24hPcnt', 0)) * 100

            # 3. Fetch Sentiment (Fear & Greed)
            sentiment = self.get_fear_and_greed()

            return {
                "current_price": current_price,
                "price_change_24h": round(price_change_24h, 2),
                "price_change_7d": round(price_change_7d, 2),
                "total_volume_24h": float(ticker_data['turnover24h']),
                "sentiment": sentiment # Dictionary with fng_score and fng_label
            }

        except Exception as e:
            print(f"Error fetching combined market data: {e}")
            return None

