# filepath: c:\Users\coco\Documents\codigo\background-remover-casero\test\test.py
import requests
import xml.etree.ElementTree as ET
from time import sleep
from urllib.parse import urlparse
import os

xml_url = "https://gethatch.com/feeds/53143/affiliate_53143_GB_feed_A.xml"
output_file = "test/temp_feed.xml"
api_url = "http://127.0.0.1:5000/remove-background"
errors = 0
recorrido = 0

def download_xml(url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP 4xx/5xx
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"XML downloaded successfully and saved to {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading XML: {e}")

def extract_image_urls(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    image_urls = []

    # Asumiendo que cada producto está en un elemento <product> y la URL de la imagen está en un elemento <image-url>
    for product in root.findall('.//product'):
        image_url = product.find('image-url')
        if image_url is not None:
            image_urls.append(image_url.text)

    return image_urls

def process_images(image_url):
    global errors
    global recorrido
    recorrido += 1

    parsed_url = urlparse(image_url)
    file_name_with_extension = os.path.basename(parsed_url.path)
    input_path, _  = os.path.splitext(file_name_with_extension)
    print("image: ", input_path, image_url)
    peticion = {'image_url': image_url, "route_to_save": "testing_remover/", "file_name": input_path + '.png'}  
    try:
        response = requests.post(api_url, json=peticion)
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP 4xx/5xx
        print(f"Processed image URL: {image_url}")
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        errors += 1
        print(f"Error processing image URL {image_url}: {e}")

if __name__ == "__main__":
    download_xml(xml_url, output_file)
    image_urls = extract_image_urls(output_file)
    
    # for image_url in image_urls:
    # esperar 1 segundo
    # sleep(1)
    #     process_images(image_url)

    for i in range(0, 10):
       process_images(image_urls[i])

    print("----------------")
    print("Cantidad de imagenes a procesar: ",  len(image_urls))
    print("Cantidad de imagenes procesadas: ", recorrido)
    print("Errores: ", errors)
