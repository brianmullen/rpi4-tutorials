from socket import socket, AF_INET, SOCK_DGRAM

bufferSize=1024
msgFromClient='Howdy Server, from Your Client'
bytesToSend=msgFromClient.encode('utf-8')

serverAddress='192.168.1.28'
serverPort=2222

clientSocket=socket(AF_INET, SOCK_DGRAM)
# clientSocket.sendto(bytesToSend, (serverAddress, serverPort))
# print('Client sent message')

while True:
    command=input('What do you want to do, INC or DEC? ')
    bytesToSend=command.encode('utf-8')
    clientSocket.sendto(bytesToSend, (serverAddress, serverPort))
    message,address=clientSocket.recvfrom(bufferSize)
    message=message.decode('utf-8')
    print(message)
    print('Server Address: ', address[0], address[1])
