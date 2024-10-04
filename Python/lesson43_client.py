from socket import socket, AF_INET, SOCK_DGRAM

bufferSize=1024
serverAddress='192.168.1.28'
serverPort=2222
clientSocket=socket(AF_INET, SOCK_DGRAM)

while True:
    command=input('What do you want to know, TEMP or HUM?')
    bytesToSend=command.encode('utf-8')
    clientSocket.sendto(bytesToSend, (serverAddress, serverPort))
    message,address=clientSocket.recvfrom(bufferSize)
    message=message.decode('utf-8')
    
    if command == 'TEMP':
        print('Temperature:', message)
    elif command == 'HUM':
        print('Humidity:', message)
    else:
        print(message)
