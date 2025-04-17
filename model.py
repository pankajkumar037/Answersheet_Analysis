from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError
# Load environment variables
from PyPDF2 import PdfReader  # A
import os
load_dotenv()
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

# Configure Gemini model
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    raise RuntimeError(f"Failed to configure Generative AI model: {str(e)}")

# Model output functions
def model_output_with_image(image: Image.Image, prompt: str):
    try:
        response = model.generate_content([image, prompt])
        return response.text
    except UnidentifiedImageError:
        return "Error: The provided image file is not a valid image."
    except Exception as e:
        return f"An error occurred while processing the image: {str(e)}"

def model_output_text(prompt: str):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating text: {str(e)}"
    

def model_output_with_pdf(pdf_file, prompt: str):
    try:
        reader = PdfReader(pdf_file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        combined_prompt = f"{prompt}\n\nExtracted PDF Content:\n{text}"
        response = model.generate_content(combined_prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while processing the PDF: {str(e)}"