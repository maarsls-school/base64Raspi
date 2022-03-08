from io import BytesIO
from time import sleep
from picamera import PiCamera
import base64
from PIL import Image

image = Image.new("RGB", (300, 50))
# Create an in-memory stream
my_stream = BytesIO()
camera = PiCamera()
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture(my_stream, 'jpeg')
image.save(my_stream, 'PNG')
base64S = base64.b64encode(my_stream.getvalue()).decode()
print(base64S)
