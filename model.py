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

import io

def model_output_with_image(uploaded_file_or_image, prompt):
    try:
        #  input is a PIL Image (not a Streamlit UploadedFile), converting it to bytes
        if isinstance(uploaded_file_or_image, Image.Image):
            buffer = io.BytesIO()
            uploaded_file_or_image.save(buffer, format="JPEG")
            buffer.seek(0)
            uploaded_file = buffer
        else:
            uploaded_file_or_image.seek(0)
            uploaded_file = uploaded_file_or_image

        base64_image = base64.b64encode(uploaded_file.read()).decode("utf-8")
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
