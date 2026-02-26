from src.news_node import CryptoPanicMiner
from src.research_node import ResearchMiner
from src.macro_node import MacroMiner
from src.analyzer import MarketAnalyzer

def run_agent():
    print("🤖 AgenticAlpha is waking up...")
    
    # --- Step 1: Data Ingestion ---
    print("📥 Fetching Market News...")
    news_agent = CryptoPanicMiner()
    news_data = news_agent.get_recent_news(days_limit=2, filter_type="important", max_results=10)

    print("📥 Fetching On-Chain Research...")
    research_agent = ResearchMiner()
    research_data = research_agent.get_latest_research(limit=3)

    print("📥 Fetching Macroeconomic Data...")
    macro_agent = MacroMiner()
    macro_data = macro_agent.get_latest_macro(limit_per_feed=2)

    # Check if we have enough data to proceed
    if not news_data and not research_data and not macro_data:
        print("❌ Failed to fetch data. Aborting analysis.")
        return

    # --- Step 2: AI Processing ---
    print("🧠 Analyzing data streams with Gemini...")
    analyzer = MarketAnalyzer()
    final_analysis = analyzer.generate_trading_signal(news_data, research_data, macro_data)

    # --- Step 3: Output ---
    print("\n=========================================")
    print("       📊 AGENTIC ALPHA REPORT 📊       ")
    print("=========================================\n")
    print(final_analysis)
    print("\n=========================================")

if __name__ == "__main__":
    run_agent()