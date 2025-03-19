import time
import os
from rembg import remove
import requests
import urllib.request
import boto3
from datetime import datetime
from urllib.parse import urlparse

#carpeta temporal para guardar las imagenes
#temp_folder = os.path.join(os.getcwd(), 'temp') + '/'
temp_folder = 'temp/'

def remove_background_image(input_path, file_name=None):

    if file_name:
        output_path =  temp_folder + file_name
    else:   
        output_path =  input_path.split('.')[0] + '_nobg.png'
    
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
            if not input_data:
                raise ValueError("El archivo está vacío o corrupto")
            output_data = remove(input_data)
            with open(output_path, 'wb') as o:
                o.write(output_data)
        print(f"Background removed successfully: {input_path}")
        return output_path
    except Exception as e:
        print(f"Error removing background: {e}")
        return None

def renameImageUrl(image_url, rename=False):
    #chequeo que no este vacio
    if not image_url:
        return 'empty-url'
    
    #chequeo que sea un string
    if not isinstance(image_url, str):
        return 'not-url'

    #chequeo que sea una url
    if not image_url.startswith('http'):
        return 'not-url'
    
    if rename:
        #agrego nombre extrayendo extension y poniendo fecha y hora de hoy
       
        now = datetime.now()
        #renombro con la fecha de hoy + la extension
        input_path = now.strftime("%Y%m%d%H%M%S") + '.' + image_url.split('.')[-1]
        #agrego carpeta temp al nombre
        input_path = temp_folder + input_path
    else:
        #extraer de la url el nombre y la extension
        parsed_url = urlparse(image_url)
        input_path = os.path.basename(parsed_url.path)
        #agrego carpeta temp al nombre
        input_path = temp_folder + input_path
    return input_path

def downloadImageFromURL(image_url, input_path, max_retries=5):
    headers = {'User-Agent': 'Mozilla/5.0'}
    attempt = 0
    while attempt < max_retries:
        try:
            with requests.get(image_url, headers=headers, stream=True) as response:
                response.raise_for_status()
                with open(input_path, 'wb') as out_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        out_file.write(chunk)
            print(f"Downloaded image successfully: {image_url}")
            return input_path
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Error downloading image (attempt {attempt}/{max_retries}): {e}")
            time.sleep(2)  # Esperar 2 segundos antes de reintentar
    print(f"Failed to download image after {max_retries} attempts: {image_url}")
    return None

def deleteFile(file_path):
    #espero 2 segundos
    time.sleep(2)
    #borro el archivo
    os.remove(file_path)
    return True

def uploadS3(file_path, bucket_name, object_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, object_name)
    return True