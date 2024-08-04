from PIL import Image
import pytesseract
import os

def process_image(file):
    file_path = os.path.join('static/uploads', file.filename)
    file.save(file_path)
    extracted_text = pytesseract.image_to_string(Image.open(file_path))
    return file_path, extracted_text
