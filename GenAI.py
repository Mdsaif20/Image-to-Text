import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")

# Directly embed your API key (NOT RECOMMENDED)
#   # Replace with your actual API key

# Configure the API key for Google Generative AI
genai.configure(api_key=API_KEY)

def upload_to_gemini(path):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path)
    return file

generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 32,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def process_image(file_path):
    print("Processing image:", file_path)
    gemini_file = upload_to_gemini(file_path)
    prompt = "extract the text from the image separated with '|' symbol and only give table"
    response = model.generate_content([gemini_file, prompt])
    output = response.text
    lines = output.split('\n')
    rows = [line.split('|') for line in lines if line.strip()]

    if len(rows) > 1:
        df = pd.DataFrame(rows[1:], columns=rows[0])
        print("DataFrame created:", df)
        return df
    else:
        print("Gemini did not return valid table data")
        return pd.DataFrame()