from transformers import MarianTokenizer, MarianMTModel
import os

model_path = r'C:\NMT\src\models\saved_model'

if not os.path.isdir(model_path):
    raise ValueError(f"La ruta al modelo no existe: {model_path}")

try:
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    model = MarianMTModel.from_pretrained(model_path)
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo: {e}")

def translate_text(text):
    if text:
        inputs = tokenizer.encode(text, return_tensors='pt').to(model.device)
        translated = model.generate(inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text
    return ''
