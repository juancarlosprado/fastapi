# con os podemos leer la carpeta, json podemos convertir el diccionario en json
import os
import json
import zipfile
# leemos el directorio y creamos un diccionario donde guardaremos las variables

# dic = primer directorio donde lee los archivos 
# dic2 = primer directorio donde se guardalos archivos


def crear_json(dic,dic2):
    lista_archivos = os.listdir(dic)  
    for archivos in lista_archivos:
        archivo_json = {}
        # le damos la ruta para que comience a leer los archivos
        ruta = dic+archivos
        with open(ruta) as archivo_leer:
            iterador_item = 0
            for linea in archivo_leer:
                # le la linea e identifica las variables para el diccionario
                long_linea = len(linea)
                identificador = "|"
                posicion = linea.find(identificador)
                clave = linea[0:posicion]
                valor = linea[(posicion+1):(long_linea-2)]                
                #En caso de multiples items
                if (clave == "item"):
                    clave = clave+"_"+str(iterador_item)
                    iterador_item = iterador_item+1
                    text = linea[(posicion):(long_linea-1)]
                    valor = item(text,identificador)
                archivo_json[clave] = valor
        # le la linea para darle nombre al archivo
        identificador = "."
        posicion = archivos.find(identificador)
        clave = archivos[0:posicion]+".json"
        ruta = dic2+clave
        # creamos el archivo json con el diccionario
        with open(ruta, 'w') as file:
            json.dump(archivo_json, file, indent=4)

#folder_path = parámetro la ruta de la carpeta
#zip_path = donde queremos guardar el archivo zip 

def crear_zip(carpeta_a_comprimir, archivo_zip):
    with zipfile.ZipFile(archivo_zip, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Recorre la carpeta a comprimir y agrega cada archivo a la estructura del archivo zip
        for root, dirs, files in os.walk(carpeta_a_comprimir):
            for file in files:
                zip_file.write(os.path.join(root, file))


def item(text,identificador):
    item = {}
    identificador = identificador
    posiciones = [i for i, l in enumerate(text) if l == identificador]
    contador = len(posiciones)
    i=0
    array=["unidad_de_medida","codigo","descripcion","cantidad","valor_unitario","precio_unitario","descuento","subtotal","tipo_de_igv","igv","total","anticipo_regularizacion","anticipo_documento_serie","anticipo_documento_numero","codigo_producto_sunat","otros_cargos","isc","isc_linea","icbper","ivap"]
    while(i<contador-1):
        inicial = posiciones[i]+1
        final = posiciones[(i+1)]
        item[array[i]]=text[inicial:final]
        i=i+1
    return item
