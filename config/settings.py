import os
try:
    from dotenv import load_dotenv
except ImportError:
    raise ImportError("python-dotenv is required. Please install it with 'pip install python-dotenv'.")

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# Add more config variables as needed
