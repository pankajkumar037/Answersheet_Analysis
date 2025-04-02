import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

def model_output_with_image(image_path,prompt):
    image = Image.open(image_path)
    response = model.generate_content([image, prompt])
    return response.text

def model_output_text(prompt):
    response = model.generate_content(prompt)
    return response.text

