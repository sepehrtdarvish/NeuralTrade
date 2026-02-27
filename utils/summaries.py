from utils.metis_client import MetisClient
from config import config

def get_summary(raw_text):
    """
    Analyzes and summarizes financial news text using the MetisClient.
    Uses the model defined in config.ANALYSIS_MODEL_NAME.
    """
    metis = MetisClient()
    
    prompt = f"""
        Summarize the text below to minimize token count. 
        Rules:
        1. Keep all numerical data, dates, and financial figures.
        2. Keep all named entities (companies, people, assets).
        3. Remove all fluff, adjectives, and conversational fillers.
        4. Use a dense, bullet-point or telegram-style format.
        5. Output must be as short as possible without losing the core facts.

        TEXT:
        {raw_text}
        """
    
    # We use a lower temperature (0.1) for more factual and less creative financial summaries
    result = metis.send(
        prompt=prompt,
        model=config.SUMMARIES_MODEL_NAME,
        generation_config={
            "temperature": 0.1,
            "max_output_tokens": 1000
        }
    )
    
    return result