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
    route_to_save = data.get('route_to_save')
    bucket = data.get('bucket')
    file_name = data.get('file_name')

    # nombro archivo
    if file_name:
        input_path = renameImageUrl(image_url)
    else:
        input_path = renameImageUrl(image_url, True)
    
    # Descargar archivo y guardar local con el nuevo nombre
    downloadImageFromURL(image_url, input_path)
    
   
    # Remuevo el fondo
    if file_name:
        result = remove_background_image(input_path, file_name)
    else:
        result = remove_background_image(input_path)

    # Eliminar el archivo original
    deleteFile(input_path)

    # Obtener las variables de entorno
    #chequear si viene el bucket
    if bucket:
        bucket_name = bucket
    else:
        bucket_name =  os.getenv('S3_BUCKET_NAME')

    if route_to_save:
        bucket_folder = route_to_save
    else:
        bucket_folder = os.getenv('AWS_BUCKET_FOLDER')

    # Construir el object_name con la carpeta del bucket
    object_name = os.path.join(bucket_folder, os.path.basename(result))
    print(input_path, object_name, bucket_name, result)
    
    # Subir el archivo a S3
    s3url = uploadS3(result, bucket_name, object_name)
   
    # Eliminar el archivo resultante después de subirlo a S3
    deleteFile(result)
    
    if not s3url:
        return jsonify({'error': 'Error uploading to S3'}), 500

    return jsonify({'result': os.getenv('AWS_DOMAIN') + object_name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't'])