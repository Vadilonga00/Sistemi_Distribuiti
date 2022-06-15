import socket
from sys import argv
from cmd import Cmd
from threading import Thread
import json

class myPrompt(Cmd):
    prompt = '>'
    intro = 'Ciao, benvenuto nel mio prompt:'

    def __init__(self):
        super().__init__()
        self.socket = clientsocket
        self.is_connect = True
        self.topic_message = {}
        self.threading = []

    @staticmethod
    def do_ciao(inp):
        print('Ciao a te')

    def do_showtopic(self, inp):
        """
        Shows the topics to which the client is subscribed and all
        messages exchanged
        """
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

    def do_exit(self, inp):
        print('Ciao e alla prossima!')
        self.close()
        return True

    def do_subscribe(self, inp):
        """
        Subscribes the client to the topic and in case it does not exist
        creates it
        param inp: The input is the topic's name given by the user
        """
        if self.is_connect:
            if str(inp) not in self.topic_message:
                messaggio = '[SUBSCRIBE] {"topic": "%s"}' % inp
                self._sendall2(messaggio)
                self.topic_message[inp] = []
            else:
                print(f'Already subscribed to the topic!')

    def do_unsubscribe(self, inp):
        """
        Unsubscribes the client from the topic, if the client is not 
        subscribed to the given topic sends an error message
        param inp: The input is the topic's name given by the user
        """
        if self.is_connect:
            if str(inp) in self.topic_message:
                messaggio = '[UNSUBSCRIBE] {"topic": "%s"}' % inp
                self._sendall2(messaggio)
                del self.topic_message[inp]
            else:
                print(f'Error! You are not subscribed to this topic!')

    def do_send_message(self, inp):
        if self.is_connect:
            inp = inp.split('&') # modificare per inviare messagi di più parole
            topic = inp[0].strip()
            message = inp[1].strip()
            messaggio = '[SEND] {"topic": "%s", "message": "%s"}' % (topic, message)
            self._sendall2(messaggio)

    def _buffer(self,a):
        a = json.loads(a)
        print(a)
        print(type(a))
        self.topic_message[a['topic']].append([a['id'],a['messaggio']])
        print(self.topic_message)

    def _receive_message(self, clientsocket):
        while self.is_connect:
            try:
                data = clientsocket.recv(1024)
                if not data:
                    print("Connection lost with broker!")
                    self.do_disconnect(None)
                else:
                    a = data.decode('UTF-8')
                    print(a)
                    print(type(a))
                    if a[0] == '{':
                        self._buffer(a)
            except:
                print('error')

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