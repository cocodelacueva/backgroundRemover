# Background remover housemade

virtualenv venvDir
.\venvDir\Scripts\activate
.\venvDir\Scripts\deactivate

pip freeze > requirements.txt

Libreria probada
https://github.com/danielgatis/rembg?tab=readme-ov-file

## ¿cómo funciona?

Llamar al endpoint "/remove-background" por POST con estos parámetros:
´´´json
{
    "image_url": "https://helios-i.mashable.com/imagery/articles/05djrP5PjtVB7CcMtvrTOAP/images-4.fill.size_2000x1125.v1723100793.jpg",
    "route_to_save": "testing_remover/",
    "bucket" : "skuapi",
    "file_name": "prueba_compu_sin_fondo.png"
}
´´´
El unico obligatorio es image_url. si los otros no estan se va a guardar en los valores por defectos ubicados en el archivo env. 
S3_BUCKET_NAME=skuapi
AWS_REGION=us-east-2
AWS_DOMAIN=https://skuapi.s3.us-east-2.amazonaws.com/
AWS_BUCKET_FOLDER=testing_remover/

## probando

cuando probar
Error processing image URL https://images.icecat.biz/img/gallery/953070da0e239847fa78356c02f8ce1d06448592.jpg: ('Connection aborted.', ConnectionResetError(10054, 'Se ha forzado la interrupción de una conexión existente por el host remoto', None, 10054, None))
----------------
Cantidad de imagenes a procesar:  563
Cantidad de image 563
errores 484

deberian haber 79 imagenes y hay 79 imagenes
chequear q tal quedaron