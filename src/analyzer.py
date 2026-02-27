from utils import MetisClient

class MarketAnalyzer:
    def __init__(self):
        # Configure Gemini via Metis AI Gateway
        self.model = MetisClient()

    def generate_trading_signal(self, news_data, research_data, tech_data):
        # Format the technical string including Sentiment
        fng_info = f"{tech_data['sentiment']['fng_score']} ({tech_data['sentiment']['fng_label']})"
        
        tech_text = f"""
        --- CURRENT MARKET METRICS ---
        Price: ${tech_data['current_price']:,.2f}
        24h Change: {tech_data['price_change_24h']}%
        7d Change: {tech_data['price_change_7d']}%
        24h Volume: ${tech_data['total_volume_24h']:,.0f}
        Market Sentiment (Fear & Greed): {fng_info}
        """

        # (Keep news_text and research_text formatting as before)

        system_prompt = f"""
        Act as a Senior Quantitative Strategist. Your goal is a 3-14 day Swing Trade signal for Bitcoin.
        
        DATA ANALYSIS HIERARCHY:
        1. SENTIMENT & MOMENTUM: Use the Fear & Greed Index + 7d Change to identify overbought/oversold conditions. 
           (e.g., Extreme Fear at support levels is often a BUY catalyst).
        2. ON-CHAIN FILTER: Ensure the mid-term trend (Glassnode) isn't heavily bearish before calling a Long.
        3. NEWS CATALYST: Check if recent news supports or contradicts the technical momentum.

        DATA INPUTS:
        {tech_text}
        {news_data}
        {research_data}

        OUTPUT FORMAT:
        📈 FINAL SIGNAL: [BULLISH / BEARISH / NEUTRAL]
        🎯 CONFIDENCE: [0-100]%
        🔍 REASONING: (3 bullet points max)
        💡 ACTION: (Specific spot trading advice)
        """

        try:
            # Generate the response
            response = self.model.send(prompt=system_prompt)
            return response
        except Exception as e:
            return f"Error connecting to AI model: {e}"