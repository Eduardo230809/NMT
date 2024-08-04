from flask import render_template, request, jsonify
from ..services.text import translate_text
from ..services.image import process_image
from ..services.audio import process_audio
from . import main_bp

# Ruta para la página principal
@main_bp.route('/')
def index():
    return render_template('index.html')

# Ruta para traducir texto
@main_bp.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text')
    translated_text = translate_text(text)
    return jsonify({'translated_text': translated_text})

# Ruta para subir y procesar imagen
@main_bp.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('file')
    if file:
        image_url, extracted_text = process_image(file)
        return jsonify({'image_url': image_url, 'extracted_text': extracted_text})
    return jsonify({'error': 'File upload failed'})

# Ruta para subir y procesar audio
@main_bp.route('/upload_audio', methods=['POST'])
def upload_audio():
    file = request.files.get('audio')
    if file:
        audio_url, original_text = process_audio(file)
        return jsonify({'original_text': original_text, 'audio_url': audio_url})
    return jsonify({'error': 'Audio upload failed'})

# Ruta para traducir texto extraído de audio
@main_bp.route('/translate_audio', methods=['POST'])
def translate_audio():
    text = request.form.get('text')
    translated_text = translate_text(text)
    return jsonify({'translated_text': translated_text})
