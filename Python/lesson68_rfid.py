from time import sleep
from _App import App
from mfrc522 import SimpleMFRC522

def main():
    fps = 0.2
    reader = SimpleMFRC522()
    
    while True:
        command = input('Dp you want to read or write? (R or W) ')
        
        if command == 'W':
            text = input('Input your text: ')
            print('Place device by reader')
            reader.write(text)
        elif command == 'R':
            print('Place device by reader')
            id, text = reader.read()
            print('ID: ', id)
            print('Text: ', text)
            sleep(fps)

app = App()
app.main = lambda: main()
app.run()
