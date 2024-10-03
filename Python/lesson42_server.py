from socket import socket, AF_INET, SOCK_DGRAM
import dht11
from _App import App

def main():
    sensor = dht11.DHT11(17)
    bufferSize=1024
    serverAddress='192.168.1.28'
    serverPort=2222
    serverSocket=socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverAddress, serverPort))
    print('Server is listening')

    while True:
        command,clientAddress=serverSocket.recvfrom(bufferSize)
        command=command.decode('utf-8')
        print(command)
        print('Client Address:', clientAddress[0], 'Port:', clientAddress[1])
        
        if command == 'GO':
            result = sensor.read()
            if result.is_valid():
                data=str(round(result.temperature * (9.0/5.0) + 32, 1)) + ':' + str(round(result.humidity, 1))
                bytesToSend=data.encode('utf-8')
                serverSocket.sendto(bytesToSend, clientAddress)
            else:
                data='Bad Measurement'
                print(data)
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
