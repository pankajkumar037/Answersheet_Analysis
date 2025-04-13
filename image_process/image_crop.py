import streamlit as st
import numpy as np
from PIL import Image, ExifTags

def auto_orient_image(image):
    try:
        exif = image._getexif()
        if exif is not None:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            orientation_value = exif.get(orientation)

            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass

    return image


def crop_marks_section(uploaded_image):
    #image = Image.open(uploaded_image)
    image = auto_orient_image(uploaded_image)

    width, height = image.size
    box = (int(width * 0.42), 0, int(width * 0.80), height) #taking only marks part
    cropped_image = image.crop(box)

    gray = cropped_image.convert('L')

    
    gray_array = np.array(gray) / 255.0


    normalized_array = (gray_array * 255).astype(np.uint8)

    normalized_gray_image = Image.fromarray(normalized_array)

    final_rgb_image = normalized_gray_image.convert('RGB')

    return final_rgb_image


