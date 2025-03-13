from flask import Flask, request, jsonify
from src.utils import uploadS3, remove_background_image, renameImageUrl, downloadImageFromURL, deleteFile
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'msg': 'Hello, World!'})

@app.route('/remove-background', methods=['POST'])
def remove_background():
    data = request.json
    image_url = data.get('image_url')

    # Renombro archivo
    input_path = renameImageUrl(image_url)
    # Descargar archivo y guardar local con el nuevo nombre
    downloadImageFromURL(image_url, input_path)
    
    # Remuevo el fondo
    result = remove_background_image(input_path)

    # Eliminar el archivo original
    deleteFile(input_path)

    # Obtener las variables de entorno
    bucket_name = os.getenv('S3_BUCKET_NAME')
    bucket_folder = os.getenv('AWS_BUCKET_FOLDER')

    # Verificar que las variables de entorno no sean None
    if not bucket_name or not bucket_folder:
        return jsonify({'error': 'S3_BUCKET_NAME or AWS_BUCKET_FOLDER not set in environment variables'}), 500

    # Construir el object_name con la carpeta del bucket
    object_name = os.path.join(bucket_folder, os.path.basename(result))
    print(object_name)
    # Subir el archivo a S3
    s3url = uploadS3(result, bucket_name, object_name)

    # Eliminar el archivo resultante después de subirlo a S3
    deleteFile(result)
    
    if not s3url:
        return jsonify({'error': 'Error uploading to S3'}), 500

    return jsonify({'result': os.getenv('AWS_DOMAIN') + object_name})

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't'])
