# filepath: c:\Users\coco\Documents\codigo\background-remover-casero\test\test.py
import requests
import xml.etree.ElementTree as ET

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
    try:
        response = requests.post(api_url, json={'image_url': image_url})
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP 4xx/5xx
        print(f"Processed image URL: {image_url}")
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        errors += 1
        print(f"Error processing image URL {image_url}: {e}")

if __name__ == "__main__":
    download_xml(xml_url, output_file)
    image_urls = extract_image_urls(output_file)
    
    for image_url in image_urls:
        process_images(image_url)

    #for i in range(0, 10):
    #    process_images(image_urls[i])
    print("----------------")
    print("Cantidad de imagenes a procesar: ", recorrido)
    print("Cantidad de imagenes procesadas: ", len(image_urls))
    print("Errores: ", errors)
