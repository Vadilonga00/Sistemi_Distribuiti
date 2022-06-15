import socket
from sys import argv
from cmd import Cmd

def managePrompt(prompt):
    prompt.cmdloop()

class myPrompt(Cmd):
    prompt = '>'
    intro = 'Ciao, benvenuto nel mio prompt:'

    def _init_(self):
        super()._init_()
        self.socket = clientsocket
        self.is_connect = True
        self.topic_message = {}
        self.threading = []

if __name__ == '__main__':
    myIP = socket.gethostbyname(socket.gethostname())
    myPORT = int(argv[1])
    brokerIP = socket.gethostbyname(socket.gethostname())
    brokerPort = int(argv[2])

    clientsocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) #viene letta dal cmd?
    clientsocket.bind((myIP, myPORT))
    clientsocket.connect((brokerIP, brokerPort))
    
    prompt = myPrompt()
    prompt.cmdloop()