import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from time import sleep
from datetime import datetime
from apiGoogle import createFile, login



def onMovement(channel):
    # Here, alternatively, an application / command etc. can be started.
    print('There was a movement!')
    camera.start_preview(fullscreen = False, window = (50,50,640,480))
    sleep(0.1)
    name = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    camera.capture('/home/pi/projet-iot/images/'+name+'.jpeg')
    camera.stop_preview()
    createFile(creds, name)


if __name__ == '__main__':

    camera = PiCamera()

    # réglage de la résolution
    camera.resolution = (1024, 768)

    # rotation de l'image (utile si la caméra est à l'envers)
    camera.rotation = 180

    SENSOR_PIN = 23

    creds = login()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PIN, GPIO.IN)

    try:
        GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=onMovement)
        while True:
            print('its ok')
            time.sleep(1)
    except KeyboardInterrupt:
        print('Finish...')
    GPIO.cleanup()