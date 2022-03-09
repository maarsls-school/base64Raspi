from io import BytesIO
from time import sleep
from picamera import PiCamera
import base64

import base64
import requests

def encode_base64(fName):
    with open(fName, 'rb') as file:
        binary_file_data = file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        return base64_encoded_data.decode('utf-8')

def decode_Base64(fName, data):
    data_base64 = data.encode('utf-8')
    with open(fName, 'wb') as file:
        decoded_data = base64.decodebytes(data_base64)
        file.write(decoded_data)

# Create an in-memory stream
my_stream = BytesIO()
camera = PiCamera()
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture(my_stream, 'jpeg')
base64S = base64.b64encode(my_stream.getvalue()).decode()
print(base64S)

j = {'name': 'image', 'ext': 'png', 'data': base64S, 'desc': 'This is an example image'}
response = requests.put('http://3.66.167.52:5000/img_meta/0' , json=j)
print(response)

response = requests.get('http://ec2-3-66-167-52.eu-central-1.compute.amazonaws.com:5000/img_meta/19')
res_json = response.json()
print(res_json)
decode_Base64('test_files/htl-logo-from-server3.png', res_json['data'])
