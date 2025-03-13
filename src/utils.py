import time
import os
from rembg import remove
import urllib.request
import boto3

#carpeta temporal para guardar las imagenes
#temp_folder = os.path.join(os.getcwd(), 'temp') + '/'
temp_folder = 'temp/'

def remove_background_image(input_path):
    output_path =  input_path.split('.')[0] + '_nobg.png'
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)
    return output_path

def renameImageUrl(image_url):
    #chequeo que no este vacio
    if not image_url:
        return 'empty-url'
    
    #chequeo que sea un string
    if not isinstance(image_url, str):
        return 'not-url'

    #chequeo que sea una url
    if not image_url.startswith('http'):
        return 'not-url'
    
    #agrego nombre extrayendo extension y poniendo fecha y hora de hoy
    from datetime import datetime
    now = datetime.now()
    #renombro con la fecha de hoy + la extension
    input_path = now.strftime("%Y%m%d%H%M%S") + '.' + image_url.split('.')[-1]
    #agrego carpeta temp al nombre
    input_path = temp_folder + input_path
    
    return input_path

def downloadImageFromURL(image_url, input_path):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(image_url, headers=headers)
    with urllib.request.urlopen(req) as response, open(input_path, 'wb') as out_file:
        data = response.read()
        out_file.write(data)
    return input_path

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