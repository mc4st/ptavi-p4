#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import socketserver
import sys
import json
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    DiccServer = {}
    def register2json(self):
        with open("register.json", 'w') as fichero_json:
            json.dump(self.DiccServer, fichero_json)

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        #self.wfile: abstrae el socket y escribe en él.
        IP = self.client_address[0]
        PORT =  self.client_address[1]
        print("IP: ", IP, "PORT: ", PORT)

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            # self.rfile: abstrae el socket y lee.
            line_bytes = self.rfile.read()
            print("El cliente nos manda: \n" + line_bytes.decode('utf-8'))
            line = line_bytes.decode('utf-8')
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            (metodo, address, sip, space, expires) = line.split()
            if metodo == "REGISTER" and "@" in address:
                print(expires)
                time_now = int(time.time()) + int(expires)
                time_expires = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_now))
                print(time_expires)
                self.DiccServer[address] = ["address: " + str(IP), "expires: " + str(time_expires)]
                self.register2json()
            if expires == "0":
                del self.DiccServer[address]
                self.register2json()
            print(self.DiccServer)
            self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n" + b"\r\n")

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.allow_reuse_address = True
    serv.serve_forever()
    serv.close()
