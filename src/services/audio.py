from pydub import AudioSegment
import speech_recognition as sr
import os

#Función para procesar un archivo de audio, convertirlo a formato WAV si es necesario, y extraer texto utilizando reconocimiento de voz.
def process_audio(file):

    # Definir la ruta donde se guardará el archivo de audio
    audio_path = os.path.join('static/uploads', file.filename)
    file.save(audio_path)

    # Convertir el archivo de audio a formato WAV si no lo está
    if not audio_path.endswith('.wav'):
        audio = AudioSegment.from_file(audio_path)
        audio_path = os.path.splitext(audio_path)[0] + '.wav'
        audio.export(audio_path, format='wav')

    # Crear una instancia del reconocedor de voz
    recognizer = sr.Recognizer()
    try:

        # Abrir el archivo de audio y capturar los datos de audio
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            # Utilizar el servicio de Google para reconocer el texto en los datos de audio
            text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        # Manejar el caso en que el audio no pueda ser entendido
        text = ""
    except Exception as e:
        # Manejar otros posibles errores
        text = f"Error: {e}"

    return audio_path, text
