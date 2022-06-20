import socket
from sys import argv
from cmd import Cmd
from threading import Thread
import json
import time
import select

class myPrompt(Cmd):
    prompt = '>'
    intro = '\n\nWelcome to the client!\n' \
            'Documentation is available by typing <help>\n\n'

    def __init__(self):
        super().__init__()
        self.socket = None
        self.is_connect = False
        self.topic_message = {}
        self.threading = []

    def do_connect(self, inp):
        if self.is_connect:
            print('Already connected to the broker!')
            return
        else:
            try:
                args = inp.split(" ")
                address = args[0]
                port = int(args[1])
                self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
                self.socket.connect((address, port))
                self.is_connect = True
                messaggio = '[CONNECT]'
                self._sendall2(messaggio)
                self.threading = Thread(target=self._receive_message, args=(self.socket,))
                self.threading.start()
            except Exception as error_type:
                self.socket = None
                self.is_connect = False
                self.topics = []
                print(f'[ERROR] -> Connection failed: {error_type}')

    def do_send_message(self, inp):
        """
        Allows the client to send a message to a particular topic in
        which it is subscribed
        :param inp: A string given by the client containing the topic
        and message separated by "&"
        """
        if self.is_connect:
            inp = inp.split('&') # modificare per inviare messagi di più parole
            topic = inp[0].strip()
            message = inp[1].strip()
            messaggio = '[SEND] {"topic": "%s", "message": "%s"}' % (topic, message)
            self._sendall2(messaggio)
        else:
            print('You are not connected to the broker! Before proceeding run a connect')

    def do_subscribe(self, inp):
        """
        Subscribes the client to the topic and in case it does not exist
        creates it
        :param inp: The input is the topic's name given by the user
        """
        if self.is_connect:
            if str(inp) not in self.topic_message:
                messaggio = '[SUBSCRIBE] {"topic": "%s"}' % inp
                self._sendall2(messaggio)
                self.topic_message[inp] = []
            else:
                print(f'Already subscribed to the topic!')
        else:
            print('You are not connected to the broker! Before proceeding run a connect')

    def do_unsubscribe(self, inp):
        """
        Unsubscribes the client from the topic, if the client is not
        subscribed to the given topic sends an error message
        :param inp: The input is the topic's name given by the user
        """
        if self.is_connect:
            if str(inp) in self.topic_message:
                messaggio = '[UNSUBSCRIBE] {"topic": "%s"}' % inp
                self._sendall2(messaggio)
                del self.topic_message[inp]
            else:
                print(f'Error! You are not subscribed to this topic!')
        else:
            print('You are not connected to the broker! Before proceeding run a connect')


    def do_showtopic(self, inp):
        """
        Shows the topics to which the client is subscribed and all
        messages exchanged
        """
        print(self.topic_message)

    def do_disconnect(self, inp):
        """
        Makes the disconnection between broker and client
        """
        if self.is_connect and self.socket:
            self.is_connect = False
            self.threading.join()
            messaggio = '[DISCONNECT]'
            self._sendall2(messaggio)
            self.socket.close()
            self.topic_message = {}

    def do_exit(self, inp):
        """
        Disconnects the client from the broker and closes the console
        """
        self.do_disconnect(None)
        print('Ciao e alla prossima!')
        self._close()
        return True

    #UTILS METHODS
    def _receive_message(self, clientsocket):
        while self.is_connect:
            try:
                received = False
                clientsocket.setblocking(0)
                ready = select.select([clientsocket], [], [], 2.0)
                if ready[0]:
                    data = clientsocket.recv(4096)
                    received = True
                if received:
                    a = data.decode('UTF-8')
                    print(a)
                    print(type(a))
                    if a[0] == '{':
                        self._buffer(a)
            except:
                print('errore')
    
    def _sendall2(self, messaggio):
        """
        allows the sending of the input message encoding it with utf-8
        :param messaggio:  The message that the client must send to the
         broker
        """
        self.socket.sendall(messaggio.encode('UTF-8'))

    def _buffer(self,a):
        """
        Allows you to save communications sent in a given topic by specifying
        the sender id and the content of the message
        :param a: A string containing the sender id, the topic and the content
        of the message
        """
        a = json.loads(a)
        print(a)
        print(type(a))
        self.topic_message[a['topic']].append([a['id'],a['messaggio']])
        print(self.topic_message)

    def _close(self):
        if self.is_connect and self.socket:
            self.socket.close()

if __name__ == '__main__':
    myIP = socket.gethostbyname(socket.gethostname())
    myPORT = int(argv[1])
    brokerIP = socket.gethostbyname(socket.gethostname())
    brokerPort = int(argv[2])

    prompt = myPrompt()
    prompt.do_connect('%s %s' % (brokerIP, brokerPort))
    prompt.cmdloop()