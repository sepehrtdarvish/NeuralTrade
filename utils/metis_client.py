import google.generativeai as genai
from google.api_core.client_options import ClientOptions
from config import config

class MetisClient:
    def __init__(self, api_key=None, endpoint=None):
        """
        Initializes the Metis AI Gateway configuration and authentication.
        If arguments are not provided, it falls back to the values in config.py.
        """
        self.api_key = api_key or config.METIS_API_KEY
        self.endpoint = endpoint or config.API_ENDPOINT
        
        # Set the custom Metis endpoint
        client_options = ClientOptions(api_endpoint=self.endpoint)
        
        # Configure the generative AI library using the REST transport layer
        genai.configure(
            api_key=self.api_key,
            transport="rest",
            client_options=client_options
        )

    def send(self, prompt: str, model: str = None, **kwargs):
        """
        Sends a prompt to the specified model and returns the generated text.
        The **kwargs allow passing additional parameters like generation_config.
        """
        # Use the default model from config.py if no model is specified
        target_model = model or config.MODEL_NAME
        
        try:
            # Instantiate the target generative model
            genai_model = genai.GenerativeModel(target_model)
            
            # Generate content based on the prompt
            response = genai_model.generate_content(prompt, **kwargs)
            return response.text
            
        except Exception as e:
            return f"Error connecting to Metis Gateway: {e}"