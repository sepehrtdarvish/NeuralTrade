import google.generativeai as genai
from google.api_core.client_options import ClientOptions
from config import config

class MarketAnalyzer:
    def __init__(self):
        # Configure Gemini via Metis AI Gateway
        genai.configure(
            api_key=config.METIS_API_KEY,
            transport='rest',
            client_options=ClientOptions(api_endpoint=config.API_ENDPOINT)
        )
        self.model = genai.GenerativeModel(config.MODEL_NAME)

    def generate_trading_signal(self, news_data, research_data, macro_data):
        """
        Combines data from all 3 nodes and requests a swing-trading analysis from the LLM.
        """
        # 1. Format News Data
        news_text = "--- SHORT-TERM NEWS & SENTIMENT ---\n"
        for i, item in enumerate(news_data, 1):
            news_text += f"{i}. {item['title']} (Date: {item['date']})\n"

        # 2. Format On-Chain/Research Data
        research_text = "\n--- MID-TERM ON-CHAIN & FUNDAMENTALS ---\n"
        for i, item in enumerate(research_data, 1):
            research_text += f"{i}. {item['title']}\nSummary: {item['summary']}\n"

        # 3. Format Macroeconomic Data
        macro_text = "\n--- LONG-TERM MACROECONOMICS ---\n"
        for i, item in enumerate(macro_data, 1):
            macro_text += f"{i}. Source: {item['source']} | {item['title']}\nSummary: {item['summary']}\n"

        # 4. Construct the System Prompt (The Secret Sauce)
        system_prompt = f"""
        Act as an expert Quantitative Analyst and Swing Trader. Your goal is to analyze the provided data streams and output a highly logical swing trading signal (holding period: 3 to 14 days) for the general crypto market (focusing on Bitcoin).
        
        Rule 1: Ignore short-term noise. Focus on the convergence of On-chain data and Macro trends.
        Rule 2: Do NOT recommend high leverage or scalping.
        Rule 3: Be extremely concise and structured.

        Here is the collected data:
        {news_text}
        {research_text}
        {macro_text}

        Please provide your analysis in the exact following format:
        
        📈 FINAL SIGNAL: [BULLISH, BEARISH, or NEUTRAL]
        🎯 CONFIDENCE SCORE: [0 to 100]%
        
        🔍 KEY DRIVERS (Max 3 bullet points):
        - ...
        
        💡 SWING TRADE ACTION:
        [Explain what action to take right now with spot assets. E.g., "Accumulate slowly", "Hold cash", "Take profits"]
        """

        try:
            # Generate the response
            response = self.model.generate_content(system_prompt)
            return response.text
        except Exception as e:
            return f"Error connecting to AI model: {e}"