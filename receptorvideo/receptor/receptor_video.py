import cv2
import requests
import numpy as np
import re

# URL del servidor de streaming
streaming_url = 'http://127.0.0.1:5000/video_feed'  # Reemplaza con la dirección IP del servidor

# Realiza la solicitud de streaming al servidor
response = requests.get(streaming_url, stream=True)

if response.status_code == 200:
    frame_data = b''
    for chunk in response.iter_content(chunk_size=4096):
        frame_data += chunk

        # Buscar el marcador de inicio y fin de cada fotograma
        a = frame_data.find(b'\r\n\r\n')
        b = frame_data.find(b'\r\n\r\n', a+1)

        while a != -1 and b != -1:
            jpg = frame_data[a+4:b]
            frame_data = frame_data[b+4:]

            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('Video receptor', frame)

            if cv2.waitKey(1) == ord('q'):
                break

            a = frame_data.find(b'\r\n\r\n')
            b = frame_data.find(b'\r\n\r\n', a+1)

cv2.destroyAllWindows()