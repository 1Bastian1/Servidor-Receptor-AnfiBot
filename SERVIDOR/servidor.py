from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import cv2
import base64
import pandas as pd
import threading
import time
import requests
import csv
import numpy as np

"""
        public/AnalisiFisic.csv
        template/index.html
        
    El servior esta hecho en flas con la por su facilidad de levanta sistemas no complejos.

    OBJETIVO
    -------
    Su objetivo es crear un servidor de straming que envie fotogramas de una camara a traves de 
    protocolo http. Adem'as de enviar cada medio segundo un actualizaci'on del csv que esta gurdado
    en la carpeta public.

    FUNCIONALIDAD
    -------------
    Los 'socket.on' encargados de enviar una senial con el nombre que esta entre parentesis.
    Una vez alguo reciba esa senial se ejecuta la funcion que posee debajo.

    Por otro lado 'app.route' es encargado de hacer como router de las ditintas 'paginas' que 
    posee la pagina.

    'emit' encargado de emitir una senial con el nombre del primer string y puego se pasa una tupla con la 
    llave valor de lo que se quiere enviar

    OBS
    ---
    El problema de que la grabaci'on se vea en camara lenta es por que se estaba pasando el vcsv y el fotograma 
    practicamente al mismo tiempo, lo que hacia que el fotograma no se alcanzara a actualizar y se repetia
        Solucion: para el csv no es tan necesario entregar una actualizaci'on rapida por lo cual se hace
                    un spleet al blucle para que deore n poco mas que la iagen y no se solapen las instrucciones.
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
socketio = SocketIO(app)

def send_csv_data():
    while True:
        df =  pd.read_csv('public/AnalisisFisico.csv', sep='|')
        

        json_data = df.to_json()
        socketio.emit('csv_data', {'csv': json_data})
        time.sleep(500) #Se ocupan sleep distintos para que no colapsen las emisiones del csv y video

def video_stream():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = base64.b64encode(buffer.tobytes()).decode('utf-8')

        socketio.emit('video_frame', {'image': frame_bytes})
        time.sleep(0.01) #Se ocupan sleep distintos para que no colapsen las emisiones del csv y video

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_records', methods=['POST'])
def add_record():
    data = request.json
    with open('public/AnalisisFisico.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter='|')
        for register in data:
            writer.writerow(register)
    return 'Datos agregados correctamente.'

@app.route('/drop_last_record', methods=['POST'])
def drop_last_record():
    data = request.json
    data = np.array(data)
    data = data.flatten().tolist()
    df = pd.read_csv('public/AnalisisFisico.csv', sep='|')

    
    df = df[~df.isin(data).all(axis=1)]
    df.to_csv('public/AnalisisFisico.csv', sep='|', index=False)
    return "Registro eliminado"
   

    # df = pd.read_csv('public/AnalisisFisico.csv', sep='|')
    # df = df.drop(df.index[-1])
    # df.to_csv('public/AnalisisFisico.csv', sep='|', index=False)
    # return 'Dato borrado correctamente.'


@socketio.on('connect')
def client_connected():
    print('Cliente conectado :)')

    video_thread = threading.Thread(target=video_stream)
    video_thread.start()
    print(".- SENDING: video streaming")

    csv_thread = threading.Thread(target=send_csv_data)
    csv_thread.start()
    print(".- SENDING: csv data")

    

@socketio.on('disconnect')
def client_disconnected():
    print('Cliente desconectado :)')
    if not socketio.server.sockets:
        # Detener el streaming de video si no hay clientes conectados
        pass

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)