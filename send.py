from io import BytesIO
from time import sleep
from picamera import PiCamera
import base64


# Create an in-memory stream
my_stream = BytesIO()
camera = PiCamera()
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture(my_stream, 'jpeg')
base64S = base64.b64decode(my_stream)
print(base64S)
