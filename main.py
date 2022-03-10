from pir import onMovement
import paho.mqtt.client as mqtt
from picamera import PiCamera
import RPi.GPIO as GPIO
import serial,time


client = mqtt.Client()
connection = True
while connection:
    try:
        connection = client.connect("mesures.ludiksciences.fr", 1883, 60)
    except:
        print("retry in 2 seconds...")
        time.sleep(2)
        continue

def on_message(client, userdata, msg):
    arduino.write(msg.payload)
    if msg.payload.decode() == "start":
        GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=onMovement)
    elif msg.payload.decode() == "stop":
        GPIO.remove_event_detect(SENSOR_PIN)
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
client.subscribe('/robot/security')
client.on_message = on_message

SENSOR_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
    print('Running. Press CTRL-C to exit.')
    time.sleep(0.1) #wait for serial to open
    if arduino.isOpen():
        print("{} connected!".format(arduino.port))
        try:
            client.loop_start()
            while True:
                time.sleep(0.1)
                while arduino.inWaiting() == 0: pass
                if arduino.inWaiting() > 0:
                    answer = arduino.readline()
                    print(answer)
                    arduino.flushInput()
        except KeyboardInterrupt:
            print("KeyboardInterrupt has been caught.")