import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

print("\nAVAILABLE GEMINI MODELS:\n")

for model in genai.list_models():

    if "generateContent" in model.supported_generation_methods:
        print(model.name)