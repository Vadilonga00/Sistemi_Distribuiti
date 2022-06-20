# Sistemi_Distribuiti


# Index

- [Exam task](#Exam-task)
- [How to get started](#How-to-get-started)

# Exam task:

Sviluppare un client per il broker con le seguenti caratteristiche:

- il client deve collegarsi automaticamente al broker
- il client deve implementare un'interfaccia a riga di comando per:
    - collegarsi a un canale del broker
    - inviare un messaggio su un determinato canale
    - bufferizzare e fornire su richiesta all'utente la lista dei canali a cui
      si è collegati e dei messaggi in esso comunicati.
      
# How to get started:

## Before execution

Before running the client make sure you have launched the broker and get ip address and its port.
If after running the client successfully nothing happens check the firewalls of your device and network.

To execute broker.py you must:
    
   -Insert the broker port.
    
    Example of execution commands: python3 broker.py 12345
    
    In this way you will run the broker on port 12345 and the ip adress of your device.
 

## To execute

To execute client.py you must:

   -Insert the client port, the broker ip and the broker port.
   
   
    Example of execution commands: python3 client.py 1234 192.178.10.2 12345 
    
    
    In this way you will connect your client (on port 1234) to the broker (on ip 192.178.10.2 and port 12345)
    
    
# Authors
Code written by:

Carpineti Francesco, Contini Maria Elena, Vadilonga Francesca

    
