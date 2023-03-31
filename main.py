import os,shutil,zipfile
from fastapi import FastAPI, File, UploadFile
import funciones
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/uploadfile/file")
async def create_upload_file(file: UploadFile = File(...)):
    ruta ="text/"
    with open(ruta+file.filename, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

@app.post("/uploadfile/zip")
async def create_upload_file(file: UploadFile = File(...)):

    ruta ="text/"
    ruta_carpeta= ruta+(file.filename[:-4])   
    
    with open(ruta+file.filename, "wb") as f:
        f.write(await file.read())

    #crea la carpeta a descargar
    ruta_carpeta_json =ruta_carpeta+"_json"
    ruta_carpeta_xml =ruta_carpeta+"_xml"

    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    if not os.path.exists(ruta_carpeta_json):
        os.makedirs(ruta_carpeta_json)
    if not os.path.exists(ruta_carpeta_xml):
        os.makedirs(ruta_carpeta_xml)
    # Descomprimir archivo zip
    with zipfile.ZipFile(ruta+file.filename, 'r') as zip_ref:
        zip_ref.extractall(ruta_carpeta)

    
    #Le agregamos el / para que lo tome como si fuera una ruta para una carpeta
    ruta_carpeta = ruta_carpeta+"/"
    ruta_carpeta_json = ruta_carpeta_json+"/"
    ruta_zip = ruta_carpeta_json[:-1]+".zip"    
    funciones.crear_json(ruta_carpeta,ruta_carpeta_json)
    funciones.crear_zip(ruta_carpeta_json,ruta_zip) 

    #eliminando los carpetas y archivos usados
    ruta_carpeta=ruta_carpeta[:-1]
    shutil.rmtree(ruta_carpeta)
    ruta_carpeta_json=ruta_carpeta_json[:-1]
    shutil.rmtree(ruta_carpeta_json)
    ruta_carpeta = ruta_carpeta+".zip"
    os.remove(ruta_carpeta)
    
    return FileResponse(ruta_zip)
