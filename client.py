#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

if len(sys.argv) == 6:
    SERVER = 'localhost'
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    EXPIRES = int(sys.argv[5])
    metodo = sys.argv[3]
    if  metodo == 'register':
        ADDRESS = sys.argv[4]
else:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

METODO = "REGISTER"
PETICION = METODO + " " + ADDRESS + " " + "SIP/2.0" + "\r\n" + "Expires: " + str(EXPIRES) + "\r\n" + "\r\n"
print("Enviando: " + PETICION)
my_socket.send(bytes(PETICION, 'utf-8'))
data = my_socket.recv(1024) #Tamaño del Buffer 1024

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
