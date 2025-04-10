import base64
from PIL import Image, UnidentifiedImageError
from mistralai import Mistral
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY is not set in the environment variables.")

model = "pixtral-large-latest"
client = Mistral(api_key=api_key)

def encode_uploaded_image(uploaded_file):
    """Encode a Streamlit UploadedFile to base64."""
    try:
        return base64.b64encode(uploaded_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def model_output_with_image(uploaded_file, prompt):
    try:
        uploaded_file.seek(0) 
        Image.open(uploaded_file)

        uploaded_file.seek(0)
        base64_image = encode_uploaded_image(uploaded_file)
        if base64_image is None:
            return "Error: Failed to encode image."

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                ]
            }
        ]

        response = client.chat.complete(model=model, messages=messages)
        return response.choices[0].message.content

    except UnidentifiedImageError:
        return "Error: The uploaded file is not a valid image."
    except Exception as e:
        return f"An error occurred while processing the image: {str(e)}"

def model_output_text(prompt):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.complete(model=model, messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating text: {str(e)}"
