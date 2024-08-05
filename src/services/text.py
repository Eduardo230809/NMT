from transformers import MarianTokenizer, MarianMTModel
import os

# Definir la ruta al modelo guardado
model_path = r'C:\NMT\src\models\saved_model'

# Verificar si la ruta al modelo existe, de lo contrario, lanzar un error
if not os.path.isdir(model_path):
    raise ValueError(f"La ruta al modelo no existe: {model_path}")

try:
    # Intentar cargar el tokenizador desde la ruta especificada
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    # Intentar cargar el modelo desde la ruta especificada
    model = MarianMTModel.from_pretrained(model_path)
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo: {e}")

#Función para traducir un texto dado utilizando el modelo MarianMT.
def translate_text(text):
    if text:
        inputs = tokenizer.encode(text, return_tensors='pt').to(model.device)
        translated = model.generate(inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text
    return ''
