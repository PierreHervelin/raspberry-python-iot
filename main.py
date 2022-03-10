from pir import onMovement
from mqtt import on_message
import paho.mqtt.client as mqtt
from picamera import PiCamera
import RPi.GPIO as GPIO
import serial,time


camera = PiCamera()

# réglage de la résolution
camera.resolution = (1024,768)

# rotation de l'image (utile si la caméra est à l'envers)
camera.rotation = 180


SENSOR_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

client = mqtt.Client()
client.connect("mesures.ludiksciences.fr", 1883, 60)

client.subscribe('/robot/security')
client.on_message = on_message
client.loop_start()



with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
    time.sleep(0.1)  # wait for serial to open
    if arduino.isOpen():
        print("{} connected!".format(arduino.port))
        try:
            GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=onMovement)
            while True:
                time.sleep(0.1)
                while arduino.inWaiting() == 0: pass
                if arduino.inWaiting() > 0:
                    answer = arduino.readline()
                    print(answer)
                    arduino.flushInput()
        except KeyboardInterrupt:
            print("KeyboardInterrupt has been caught.")