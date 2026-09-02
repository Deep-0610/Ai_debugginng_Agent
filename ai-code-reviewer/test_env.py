import os
import warnings
from dotenv import load_dotenv
from google import genai

# Suppress standard warnings
warnings.filterwarnings("ignore")

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("[ERROR]: GOOGLE_API_KEY is missing from your .env file!")
else:
    print("🚀 Connecting to Google Gemini API using native client...")
    
    # Initialize official client
    client = genai.Client(api_key=api_key)

    try:
        # Use gemini-2.0-flash (the standard free tier model)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents='System test: Respond with "Environment setup successful!"',
        )
        print("\n[SUCCESS]:", response.text)
    except Exception as e:
        print("\n[ERROR]: Connection failed.")
        print("Details:", e)