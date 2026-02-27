from src.technical_node import TechnicalMiner
from src.news_node import CryptoPanicMiner
from src.research_node import ResearchMiner
from src.analyzer import MarketAnalyzer

def run_agent():
    print("🤖 AgenticAlpha: Starting Market Intelligence Loop...")
    
    # 1. Technical & Sentiment (The new core)
    tech_agent = TechnicalMiner(symbol="BTCUSDT")
    tech_data = tech_agent.get_market_data()
    
    # 2. News
    news_agent = CryptoPanicMiner()
    news_data = news_agent.get_strategic_news(days_limit=2)
    print(news_data)

    # 3. On-Chain Research
    research_agent = ResearchMiner()
    research_data = research_agent.get_latest_research(limit=2)

    if not tech_data:
        print("❌ Critical Error: Could not fetch technical data. Aborting.")
        return

    print("🧠 Processing multi-modal data with Gemini...")
    analyzer = MarketAnalyzer()
    final_report = analyzer.generate_trading_signal(news_data, research_data, tech_data)

    print("\n" + "="*45)
    print("        📊 AGENTIC ALPHA SWING REPORT")
    print("="*45)
    print(final_report)
    print("="*45)

if __name__ == "__main__":
    run_agent()