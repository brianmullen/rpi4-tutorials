from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from threading import Thread
import dht11
from _App import App

temperature=None
humidity=None

def main():
    global temperature, humidity

    sensor = dht11.DHT11(17)

    def takeMeasurement():
        global temperature, humidity

        while True:
            result = sensor.read()
            if result.is_valid():
                temperature = round(result.temperature * (9.0/5.0) + 32, 1)
                humidity = round(result.humidity, 1)
                print("Temperature:", temperature, "Humidity:", humidity)
            sleep(0.2)

    readThread = Thread(target=takeMeasurement)
    readThread.daemon = True
    readThread.start()

    bufferSize=1024
    serverAddress='192.168.1.28'
    serverPort=2222
    serverSocket=socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverAddress, serverPort))
    print('Server is listening')

    while True:
        command,clientAddress=serverSocket.recvfrom(bufferSize)
        command=command.decode('utf-8')
        
        if command == 'GO':
            if temperature is not None and humidity is not None:
                data=str(temperature) + ':' + str(humidity)
                bytesToSend=data.encode('utf-8')
                serverSocket.sendto(bytesToSend, clientAddress)
            else:
                data='No Measurement'
                bytesToSend=data.encode('utf-8')
                serverSocket.sendto(bytesToSend, clientAddress)
        else:
            data='Invalid Request'
            bytesToSend=data.encode('utf-8')
            serverSocket.sendto(bytesToSend, clientAddress)

app = App()
app.main = lambda: main()
app.run()

# ipAddress: ifconfig
