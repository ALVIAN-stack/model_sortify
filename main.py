from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import io
import os
import gdown

# === Inisialisasi Flask ===
app = Flask(__name__)

# === Auto-download model dari Google Drive ===
model_path = "model_klasifikasi_sampah.keras"
gdrive_url = "https://drive.google.com/uc?id=13gtfNnyhF1Nq8cX_JRvQBXFUaB5crIHu"  # Pastikan file ini public

if not os.path.exists(model_path):
    print("Model tidak ditemukan. Mengunduh dari Google Drive...")
    gdown.download(gdrive_url, model_path, quiet=False, fuzzy=True)

# === Load model ===
print("Loading model...")
model = load_model(model_path)
print("Model berhasil dimuat.")

# === Daftar nama kelas ===
class_names = ['cardboard', 'glass', 'metal', 'organic', 'paper', 'plastic']

# === Fungsi preprocessing gambar ===
def preprocess_image(file) -> np.ndarray:
    img = Image.open(io.BytesIO(file)).convert("RGB")
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# === Endpoint root ===
@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "API is running", "message": "Model is ready for prediction"})

# === Endpoint prediksi ===
@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        img_bytes = file.read()
        img_array = preprocess_image(img_bytes)
        prediction = model.predict(img_array)
        predicted_class = class_names[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        return jsonify({
            "predicted_class": predicted_class,
            "confidence": round(confidence * 100, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Run app (jika standalone) ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
