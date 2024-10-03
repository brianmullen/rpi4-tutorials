from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep

bufferSize=1024
serverAddress='192.168.1.28'
serverPort=2222
clientSocket=socket(AF_INET, SOCK_DGRAM)

while True:
    bytesToSend='GO'.encode('utf-8')
    clientSocket.sendto(bytesToSend, (serverAddress, serverPort))
    message,address=clientSocket.recvfrom(bufferSize)
    message=message.decode('utf-8')
    response=message.split(':')
    print('Server Address:', address[0], 'Port:', address[1])

    if len(response) == 1:
        print(response[0])
    elif len(response) == 2:
        print('Temperature:', response[0], 'Humidity:', response[1])
    
    sleep(0.2)
