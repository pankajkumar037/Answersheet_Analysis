import streamlit as st
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
    image = Image.open(uploaded_image)
    image = auto_orient_image(image)

    width, height = image.size
    box = (int(width * 0.42), 0, int(width * 0.80), height)
    cropped_image = image.crop(box)

    return cropped_image

