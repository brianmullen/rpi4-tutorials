from socket import socket, AF_INET, SOCK_DGRAM

bufferSize=1024
msgFromServer="Howdy Client, Happy to be Your Server"
bytesToSend=msgFromServer.encode('utf-8')

serverAddress='192.168.1.28'
serverPort=2222
serverSocket=socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverAddress, serverPort))
print('Server is listening')

counter=0
while True:
    message,address=serverSocket.recvfrom(bufferSize)
    message=message.decode('utf-8')
    print(message)
    print('Client Address: ', address[0])
    if message == 'INC':
        counter = counter + 1
    elif message == 'DEC':
        counter = counter - 1
    bytesToSend=str(counter).encode('utf-8')
    serverSocket.sendto(bytesToSend, address)

# ipAddress: ifconfig
