import socketio
import serial

sio = socketio.Client()

ser = serial.Serial('COM3', 9600, timeout=1)  # Replace 9600 with your baudrate

@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def message(data):
    print('Received message:', data)

comarcas = ["donostia", "debab", "debag", "goierri", "tolosa","urolak","bidasoa"]
#sio.connect('http://localhost:8050/test')
sio.connect('http://localhost:8050/test', namespaces=['/test'])
print('starting loop...')
try:
    while True:
        if ser.in_waiting > 0:  
            try:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    #print(data)
                    if data in comarcas:
                        print(data)
                        try:
                            #sio.emit('message', data)
                            sio.emit('message', data, namespace='/test')
                            print('data sent!')
                        except socketio.exceptions.ConnectionError as e:
                            print(f"Error sending data: {e}")
            except serial.SerialException as e:
                print(f"Error reading serial port: {e}")

except KeyboardInterrupt:
    print("\nInterrupted by user")
    ser.close()