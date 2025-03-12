import requests
import serial
from time import sleep



ser = serial.Serial('COM7', 9600, timeout=1)  # Replace 9600 with your baudrate

"""
ser = serial.Serial(
    port='COM7',\
    baudrate=9600,
    parity=serial.PARITY_NONE,
    timeout=0)
print("connected to: " + ser.portstr)
"""

def send_message(message):
    url = 'http://localhost:8050/api/update'
    data = {'message': message}
    response = requests.post(url, json=data)
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        print('Message sent successfully')
    else:
        print('Error sending message')

comarcas = ["donostia", "debab", "debag", "goierri", "tolosa","urolak","bidasoa"]

try:
    while True:
      if ser.in_waiting > 0:  
        data = ser.readline().decode('utf-8').strip()
        if data:
            #print(data)
            if data in comarcas:
                print(data)
                send_message(data)       
        #sleep(0.5)
        #ser.flushInput()
except KeyboardInterrupt:
    print("\nInterrupted by user")
    ser.close()