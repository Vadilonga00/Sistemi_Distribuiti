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
        """
        This command try to connect to the broker
        :param inp: Broker IP and broker Port separeted by a space
        """
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
                messaggio = '[CONNECT]'
                self._send_message(messaggio)
                self.is_connect = True
                print(f'Connected to the broker')
                self.threading = Thread(target=self._receive_message, args=(self.socket,))
                self.threading.start()
            except Exception as error_type:
                self.socket = None
                self.is_connect = False
                self.topics = []
                print(f'[ERROR] -> Connection failed: {error_type}')

    def do_message(self, inp):
        """
        Allows the client to send a message to a particular topic in
        which it is subscribed
        :param inp: Topic and message separated by font "&"
        """
        try:
            if self.is_connect:
                inp = inp.split('&') # modificare per inviare messagi di più parole
                topic = inp[0].strip()
                message = inp[1].strip()
                messaggio = '[SEND] {"topic": "%s", "message": "%s"}' % (topic, message)
                self._send_message(messaggio)
            else:
                print('You are not connected to the broker! Before proceeding run a connect')
         
        except Exception as error_type:
                print(f'[ERROR] -> Error sending message!\n Error type: {error_type}')

    def do_subscribe(self, inp):
        """
        Subscribes the client to the topic and in case it does not exist
        creates it
        :param inp: Topic's name given by the user
        """
        if self.is_connect:
            if str(inp) not in self.topic_message:
                try:
                    messaggio = '[SUBSCRIBE] {"topic": "%s"}' % inp
                    self._send_message(messaggio)
                    self.topic_message[inp] = []
                except Exception as error_type:
                    print(f'[ERROR] -> Error sending the subscription message!\n Error type: {error_type}')
                
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
                try:
                    messaggio = '[UNSUBSCRIBE] {"topic": "%s"}' % inp
                    self._send_message(messaggio)
                    del self.topic_message[inp]
                except Exception as error_type:
                    print(f'[ERROR] -> Error sending the unsubscription message!\n Error type: {error_type}')      
            else:
                print(f'Error! You are not subscribed to this topic!')
        else:
            print('You are not connected to the broker! Before proceeding run a connect')


    def do_message_history(self, inp):
        """
        Shows the topics to which the client is subscribed and all
        messages exchanged
        """
        print(self.topic_message)

    def do_disconnect(self, inp):
        """
        Makes the disconnection between broker and client
        """
        if self.is_connect:
            self.is_connect = False
            self.threading.join()
            messaggio = '[DISCONNECT]'
            self._send_message(messaggio)
            self.topic_message = {}
            self.socket.close()
            print(f'Disconnected from the broker, to log back on run connect command')

    def do_exit(self, inp):
        """
        Disconnects the client from the broker and closes the console
        """
        self.do_disconnect(None)
        print('Hello and see you next!')
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
                    if a[0] == '{':
                        self._buffer(a)
            except Exception as error_type:
                print(f'[ERROR] -> Error in receiving message!\n Error type: {error_type}')
    
    def _send_message(self, messaggio):
        """
        Allows the sending of the input message encoding it with utf-8
        :param messaggio:  The message that the client must send to the
         broker
        """
        self.socket.sendall(messaggio.encode('UTF-8'))

    def _buffer(self,a):
        """
        Allows you to save communications sent in a given topic by specifying
        the sender id and the content of the message
        :param a: Sender id, topic and the content
        of the message
        """
        a = json.loads(a)
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