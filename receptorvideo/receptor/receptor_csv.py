import requests

data =[
    ['prueba 22','asd','ads','asdasd(0).jpg','asd','asd','Aceites y lubricantes','asdasd_parte_asd.jpg','','','','','','Sin material reciclado','No Retornable','Residuo NO Peligroso','','Aceites Lubricantes No Recuperables','','','','',''],
    ['prueba 22','asd','ads','asdasd(0).jpg','asd','asd','Aceites y lubricantes','asdasd_parte_asd.jpg','','','','','','Sin material reciclado','No Retornable','Residuo NO Peligroso','','Aceites Lubricantes No Recuperables','','','','','']
]


url = "http://127.0.0.1:5000/add_row_csv" 
response = requests.post(url, json=data)
print(response.text)

