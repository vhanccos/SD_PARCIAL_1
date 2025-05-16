from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
SERVER_IMAGES = "server_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SERVER_IMAGES, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    # Muestra página principal con opciones
    server_images = os.listdir(SERVER_IMAGES)
    processed_images = os.listdir("static/processed")
    return render_template(
        "index.html", server_images=server_images, processed_images=processed_images
    )


@app.route("/server_images/<filename>")
def server_image(filename):
    # Servir imágenes que están en servidor
    return send_from_directory(SERVER_IMAGES, filename)


@app.route("/upload_image", methods=["POST"])
def upload_image():
    # Recibe imagen modificada desde cliente para guardar en servidor
    file = request.files.get("image")
    if not file:
        return jsonify({"status": "fail", "message": "No file provided"})
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    return jsonify({"status": "success", "message": f"File saved as {filename}"})


@app.route("/upload_processed", methods=["POST"])
def upload_processed():
    data = request.get_json()
    img_data = data["image"]
    filename = data.get("filename", "processed.png")

    # Convertir base64 a binario
    header, encoded = img_data.split(",", 1)
    img_bytes = base64.b64decode(encoded)

    # Guardar en una carpeta
    save_path = os.path.join("static", "processed", filename)
    with open(save_path, "wb") as f:
        f.write(img_bytes)

    return jsonify({"status": "success", "message": f"Imagen guardada como {filename}"})


if __name__ == "__main__":
    app.run(debug=True)
