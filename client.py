import socket
from sys import argv
from cmd import Cmd
from threading import Thread

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

    @staticmethod
    def do_ciao(inp):
        print('Ciao a te')

    def do_showtopic(self, inp):
        print(self.topic_message)

    def do_connect_tcp(self, inp):
        if not self.is_connect:
            args = inp.split(" ")
            address = args[0]
            port = int(args[1])
            self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            self.socket.connect((address, port))
            self.is_connect = True

    def do_connect_to_broker(self, inp):
        if self.is_connect:
            messaggio = '[CONNECT]'
            self._sendall2(messaggio)
            self.threading = Thread(target=self._receive_message, args=(self.socket,))
            self.threading.start()
            print(self.threading)

    def do_disconnect(self, inp):
        if self.is_connect:
            messaggio = '[DISCONNECT]'
            self._sendall2(messaggio)
            self.socket.close()
            self.is_connect = False
            self.topic_message = {}
        
    def do_subscribe(self, inp):
        if self.is_connect:
            if str(inp) not in self.topic_message:
                messaggio = '[SUBSCRIBE] {"topic": "%s"}' % inp
                self._sendall2(messaggio)
                self.topic_message[inp] = []
            else:
                print(f'Already subscribed to the topic!')

    def do_unsubscribe(self, inp):
        if self.is_connect:
            if str(inp) in self.topic_message:
                messaggio = '[UNSUBSCRIBE] {"topic": "%s"}' % inp
                self._sendall2(messaggio)
                del self.topic_message[inp]
            else:
                print(f'Error! You are not subscribed to this topic!')

    def do_exit(self, inp):
        print('Ciao e alla prossima!')
        self.close()
        return True

    def _close(self):
        if self.is_connect:
            self.socket.close()
        pass
    
    def _sendall2(self, messaggio):
        self.socket.sendall(messaggio.encode('UTF-8'))

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