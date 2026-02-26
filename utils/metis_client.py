# src/analyzer.py
from src.metis_client import MetisClient

class MarketAnalyzer:
    def __init__(self):
        # ساخت یک نمونه از کلاینت متیس که خودت نوشتی
        self.ai_client = MetisClient()

    def generate_trading_signal(self, news_data, research_data, macro_data):
        news_text = "--- SHORT-TERM NEWS ---\n"
        for item in news_data:
            news_text += f"- {item.get('title', '')} (Date: {item.get('date', '')})\n"

        research_text = "\n--- MID-TERM ON-CHAIN ---\n"
        for item in research_data:
            research_text += f"- {item.get('title', '')}\n"

        macro_text = "\n--- LONG-TERM MACRO ---\n"
        for item in macro_data:
            macro_text += f"- {item.get('source', '')}: {item.get('title', '')}\n"

        system_prompt = f"""
        Act as an expert Quantitative Analyst and Swing Trader.
        Analyze the following data streams and provide a swing trading signal (holding period: 3 to 14 days) for the general crypto market.
        
        Data Streams:
        {news_text}
        {research_text}
        {macro_text}

        Provide the analysis in this exact format:
        📈 FINAL SIGNAL: [BULLISH, BEARISH, or NEUTRAL]
        🎯 CONFIDENCE SCORE: [0 to 100]%
        🔍 KEY DRIVERS: (Max 3 brief bullet points)
        💡 SWING TRADE ACTION: (Clear action for spot assets, no leverage)
        """

        # ارسال پرامپت به متیس و دریافت جواب
        return self.ai_client.send(prompt=system_prompt)