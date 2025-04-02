import google.generativeai as genai
from PIL import Image, UnidentifiedImageError
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    raise RuntimeError(f"Failed to configure Generative AI model: {str(e)}")


def model_output_with_image(image_path, prompt):
    try:
        image = Image.open(image_path)
        response = model.generate_content([image, prompt])
        return response.text
    except UnidentifiedImageError:
        return "Error: The provided image file is not a valid image."
    except FileNotFoundError:
        return "Error: The specified image file was not found."
    except Exception as e:
        return f"An error occurred while processing the image: {str(e)}"


def model_output_text(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating text: {str(e)}"


