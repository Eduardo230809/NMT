from flask import Blueprint, request, jsonify, render_template, url_for
from PIL import Image
import pytesseract
import os
from pydub import AudioSegment
import speech_recognition as sr
from transformers import MarianTokenizer, MarianMTModel

# Crea un Blueprint llamado 'main' para agrupar las rutas y la lógica relacionada.
main_bp = Blueprint('main', __name__)

# Ruta al modelo de traducción guardado.
model_path = r'C:\NMT\src\models\saved_model'
# Verifica si la ruta al modelo existe. Si no, lanza un error.
if not os.path.isdir(model_path):
    raise ValueError(f"La ruta al modelo no existe: {model_path}")

try:
    # Carga el tokenizador y el modelo de traducción desde la ruta especificada.
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    model = MarianMTModel.from_pretrained(model_path)
    print("Modelo y tokenizador cargados exitosamente.")
except Exception as e:
    # Maneja cualquier error al cargar el modelo y el tokenizador.
    print(f"Error al cargar el modelo: {e}")

@main_bp.route('/')
def index():
    # Renderiza la plantilla HTML para la página principal.
    return render_template('index.html')

@main_bp.route('/translate', methods=['POST'])
def translate():
    # Obtiene el texto enviado en la solicitud POST.
    text = request.form.get('text')
    if text:
        # Codifica el texto para el modelo de traducción.
        inputs = tokenizer.encode(text, return_tensors='pt').to(model.device)
        # Genera la traducción utilizando el modelo.
        translated = model.generate(inputs)
        # Decodifica la traducción para obtener el texto en lenguaje natural.
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        # Devuelve la traducción en formato JSON.
        return jsonify({'translated_text': translated_text})
    # Devuelve una respuesta JSON vacía si no se proporciona texto.
    return jsonify({'translated_text': ''})

@main_bp.route('/upload', methods=['POST'])
def upload():
    # Obtiene el archivo enviado en la solicitud POST.
    file = request.files.get('file')
    if file:
        # Guarda el archivo en la carpeta 'static/uploads'.
        uploads_dir = os.path.join('static', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        file_path = os.path.join(uploads_dir, file.filename)
        file.save(file_path)
        # Extrae el texto de la imagen utilizando pytesseract.
        extracted_text = pytesseract.image_to_string(Image.open(file_path))

        # Traduce el texto extraído.
        inputs = tokenizer.encode(extracted_text, return_tensors='pt').to(model.device)
        translated = model.generate(inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

        # Devuelve la URL de la imagen y el texto extraído en formato JSON.
        return jsonify({
            'image_url': url_for('static', filename=f'uploads/{file.filename}'),
            'extracted_text': translated_text
        })
    # Devuelve un mensaje de error si la carga del archivo falla.
    return jsonify({'error': 'File upload failed'})

@main_bp.route('/upload_audio', methods=['POST'])
def upload_audio():
    # Obtiene el archivo de audio enviado en la solicitud POST.
    file = request.files.get('audio')
    if file:
        # Guarda el archivo de audio en la carpeta 'static/uploads'.
        audio_path = os.path.join('static/uploads', file.filename)
        file.save(audio_path)

        # Convierte el archivo de audio a WAV si no está en formato WAV.
        if not audio_path.endswith('.wav'):
            audio = AudioSegment.from_file(audio_path)
            audio_path = os.path.splitext(audio_path)[0] + '.wav'
            audio.export(audio_path, format='wav')

        # Crea un objeto reconocedor de voz.
        recognizer = sr.Recognizer()
        try:
            # Abre el archivo de audio y convierte el audio en texto.
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            # Maneja el caso en el que el audio no puede ser entendido.
            text = ""
        except Exception as e:
            # Maneja cualquier otro error que ocurra durante el reconocimiento de voz.
            text = f"Error: {e}"

        # Devuelve el texto extraído del audio y la URL del archivo de audio en formato JSON.
        return jsonify({'original_text': text, 'audio_url': audio_path})
    # Devuelve un mensaje de error si la carga del archivo de audio falla.
    return jsonify({'error': 'Audio upload failed'})

@main_bp.route('/translate_audio', methods=['POST'])
def translate_audio():
    # Obtiene el texto enviado en la solicitud POST.
    text = request.form.get('text')
    if text:
        # Codifica el texto para el modelo de traducción.
        inputs = tokenizer.encode(text, return_tensors='pt').to(model.device)
        # Genera la traducción utilizando el modelo.
        translated = model.generate(inputs)
        # Decodifica la traducción para obtener el texto en lenguaje natural.
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        
        # Devuelve la traducción en formato JSON.
        return jsonify({'translated_text': translated_text})
    # Devuelve una respuesta JSON vacía si no se proporciona texto.
    return jsonify({'translated_text': ''})
