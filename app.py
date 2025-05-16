from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
SERVER_IMAGES = 'server_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SERVER_IMAGES, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Muestra página principal con opciones
    server_images = os.listdir(SERVER_IMAGES)
    return render_template('index.html', server_images=server_images)

@app.route('/server_images/<filename>')
def server_image(filename):
    # Servir imágenes que están en servidor
    return send_from_directory(SERVER_IMAGES, filename)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Recibe imagen modificada desde cliente para guardar en servidor
    file = request.files.get('image')
    if not file:
        return jsonify({'status': 'fail', 'message': 'No file provided'})
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return jsonify({'status': 'success', 'message': f'File saved as {filename}'})

if __name__ == '__main__':
    app.run(debug=True)
