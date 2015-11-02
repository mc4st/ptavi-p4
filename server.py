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

    def json2register(self):
        try:
            with open("register.json", 'r') as existe:
                self.DiccServer = json.load(existe)
        except:
            pass

    def deleteDiccServer(self):
        new_list = []
        formato = "%Y-%m-%d %H:%M:%S +0000"
        time_now = time.time()
        print(time_now)
        for clave in self.DiccServer:
            expires = " ".join(self.DiccServer[clave][1].split(" ")[1:])
            time_now = time.strftime(formato, time.gmtime())
            if expires <= time_now:
                new_list.append(clave)
        for usuario in new_list:
            del self.DiccServer[usuario]

    def handle(self):
        """
        Escribe dirección y puerto del cliente (de tupla client_address)
        """
        IP = self.client_address[0]
        PORT = self.client_address[1]
        print("IP: ", IP, "PORT: ", PORT)

        while 1:
            """
            Leyendo línea a línea lo que nos envía el cliente
            """
            line_bytes = self.rfile.read()
            print("El cliente nos manda: \n" + line_bytes.decode('utf-8'))
            line = line_bytes.decode('utf-8')
            if not line:
                break
            (metodo, address, sip, space, expires) = line.split()
            if metodo == "REGISTER" and "@" in address:
                print(expires)
                time_now = int(time.time()) + int(expires)
                time_expires = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_now))
                print(time_expires)
                self.DiccServer[address] = ["address: " + str(IP), "expires: " + str(time_expires)]
                self.deleteDiccServer()
                self.register2json()
            if expires == "0":
                del self.DiccServer[address]
                self.register2json()
            print(self.DiccServer)
            self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n" + b"\r\n")

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.allow_reuse_address = True
    serv.serve_forever()
    serv.close()
