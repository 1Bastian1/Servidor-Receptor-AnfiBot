import cv2
import base64
import numpy as np
import socketio
import pandas as pd
from io import StringIO
import requests

url = 'http://192.168.1.137:5000'
"""
    Encargado de hacer la conexion correcta entre el anfibot y el servidor
    Cada sio,on toma un tipo de consulta del protocolo http para luego ejecutar la fucion
    que la prosigue.
    Además on_vide_fram se encarga de convertir el frmae que viaja por la red a un frame entendida
    por cv2. Al igual que on_cvs_data encargado de tomar la data en formato json y transformarla
    a formato dataframe.

    Tanto al data del csv como el frame es guardado en una variable local la cual despues
    puede ser obtenidad desde el archivo externo (anfibot)

    Es necesario cambiar la url con la ip donde este instalado y ejecutando el codigo del servidor.
"""
sio = socketio.Client()

last_frame = None
recived_csv = None

@sio.on('connect')
def on_connect():
    print('Conectado al servidor')

@sio.on('disconnect')
def on_disconnect():
    print('Desconectado del servidor')

@sio.on('video_frame')
def on_video_frame(data):
    global last_frame
    frame_bytes = base64.b64decode(data['image'])
    frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
    last_frame = frame

@sio.on('csv_data')
def on_csv_data(data):
    global recived_csv
    data_csv_serv = data['csv']
    if data_csv_serv:
        df = pd.read_json(StringIO(data_csv_serv))
        recived_csv = df
        


def conectarServidor():
    server_url = url
    sio.connect(server_url)


def desconectarServidor():
    sio.disconnect()


def sendRecords(data):
    response = requests.post(url=url+'/add_records', json=data)
    print(response.text)

def dropLastRecord(data):
    response = requests.post(url=url+'/drop_last_record', json=data)
    print(response.text)
