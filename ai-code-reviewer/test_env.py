import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    print("[ERROR]: GROQ_API_KEY is missing from your .env file!")
else:
    print("🚀 Fetching active models from Groq...")
    client = Groq(api_key=groq_key)

    try:
        # Retrieve all active models from your account
        models_page = client.models.list()
        active_models = [m.id for m in models_page.data]
        
        print(f"✅ Found {len(active_models)} available models: {active_models[:3]}")
        
        # Pick the first available model
        target_model = active_models[0]
        print(f"🧪 Testing generation with model: '{target_model}'...")

        response = client.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "user", "content": "System test: Respond with 'Environment setup successful!'"}
            ]
        )
        print("\n[SUCCESS]:", response.choices[0].message.content)

    except Exception as e:
        print("\n[ERROR]: Connection failed.")
        print("Details:", e)