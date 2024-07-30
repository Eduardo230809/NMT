import os
from transformers import MarianTokenizer, MarianMTModel
from flask import Blueprint, request, jsonify, render_template
from PIL import Image
import pytesseract
import torch

main_bp = Blueprint('main', __name__)

# Ruta al modelo local
model_path = r'C:\Users\Eduardo\Documents\Transformer\src\models\saved_model'

# Verifica que la ruta exista
if not os.path.isdir(model_path):
    raise ValueError(f"La ruta al modelo no existe: {model_path}")

# Cargar el tokenizador y el modelo desde la ruta local
try:
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    model = MarianMTModel.from_pretrained(model_path)
    print("Modelo y tokenizador cargados exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text')
    if text:
        inputs = tokenizer.encode(text, return_tensors='pt').to(model.device)
        translated = model.generate(inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        return jsonify({'translated_text': translated_text})
    return jsonify({'translated_text': ''})

@main_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        file_path = os.path.join('static/uploads', file.filename)
        file.save(file_path)
        extracted_text = pytesseract.image_to_string(Image.open(file_path))
        return jsonify({'image_url': file_path, 'extracted_text': extracted_text})
    return jsonify({'error': 'File upload failed'})
