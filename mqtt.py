#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name
import paho.mqtt.client as mqtt
import serial,time



def on_message(client, userdata, msg):
    arduino.write(msg.payload)
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


if __name__ == '__main__':

    client = mqtt.Client()
    client.connect("mesures.ludiksciences.fr", 1883, 60)

    client.subscribe('/robot/security')
    client.on_message = on_message
    client.loop_start()

    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    time.sleep(0.1)
                    while arduino.inWaiting()==0: pass
                    if  arduino.inWaiting()>0: 
                        answer=arduino.readline()
                        print(answer)
                        arduino.flushInput()
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")