import paho.mqtt.client as mqtt
import time

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

def takeAndPublish():
    # Create an in-memory stream
    my_stream = BytesIO()
    camera = PiCamera()
    # camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture(my_stream, 'jpeg')
    base64S = base64.b64encode(my_stream.getvalue()).decode()
    print(base64S)

    j = {'name': 'image', 'ext': 'png', 'data': base64S, 'desc': 'This is an example image'}
    print(j)

    response = requests.put('http://3.66.167.52:5000/img_meta/0' , json=j)
    print(response)
    res_json = response.json()
    print(res_json)

    client = mqtt.Client('88ac22e6-4ae5-4d3f-8531-358157de95d5')
    client.connect('3.66.167.52')
    client.publish("foto/taken/dev0","{'info':'imageTaken'}")


# Diese Methode wird aufgerunfen, wenn eine Nachricht fuer einen Channel hereinkommt
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

# Wenn Logging-Information fuer den Client vorhanden ist (gut fuer das Fehlersuchen)
def on_log(client, userdata, level, buf):
    print("log: ",buf)

if __name__ == '__main__':
    client = mqtt.Client('182f6dab-890e-4338-ad23-8b4d3dda362f')  # Der Parameter ist die client-ID, diese sollte möglichst eindeutig sein.
    client.connect('3.66.167.52')   # Im Moment verwenden wir die lokale mosquitto Installation, spaeter durch die IP zu ersetzen

    client.subscribe("foto/take") # Eintragen fuer einen bestimmten Channel
    client.on_message = takeAndPublish # die on_message-Methode soll aufgerfufen werden wenn einen neue Nachricht hereinkommt
    client.on_log = on_log
    client.loop_start()  # loop starten
    client.loop_forever() # loop starten in Endlosschleife (blockiert)
    print("EXIT")