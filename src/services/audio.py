from pydub import AudioSegment
import speech_recognition as sr
import os

def process_audio(file):
    audio_path = os.path.join('static/uploads', file.filename)
    file.save(audio_path)

    if not audio_path.endswith('.wav'):
        audio = AudioSegment.from_file(audio_path)
        audio_path = os.path.splitext(audio_path)[0] + '.wav'
        audio.export(audio_path, format='wav')

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = ""
    except Exception as e:
        text = f"Error: {e}"

    return audio_path, text
