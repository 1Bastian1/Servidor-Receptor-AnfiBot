from flask import Flask, render_template, Response, request, jsonify
import cv2
import csv
import jwt
from functools import wraps


app = Flask(__name__)

# Ruta de la página principal
@app.route('/')
def index():
    return render_template('index.html')#con la carpeta template flask sabe donde esta el index

# Generador de video
def generate_video():
    cap = cv2.VideoCapture(0)  # Utiliza 0 para la cámara predeterminada

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

    cap.release()

#======================
#==========CSV=========
#======================
@app.route('/add_data_csv', methods=['POST'])
def add_row_csv():
    data = request.json                     
    with open('datos.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter='|')
        for register in data:
            writer.writerow(register)
    return 'Datos agregados correctamente.'

@app.route('/obtain_csv', methods=['GET'])
def obtener_csv():
    with open('datos.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter='|')  # Establece el separador como |
        data = [dict(row) for row in reader]  # Convierte las filas en un diccionario
    return jsonify(data)




#======================
#=========VIDEO========
#======================
# Ruta para transmitir el video
@app.route('/video_feed')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)