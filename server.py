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
        formato = '%Y-%m-%d %H:%M:%S'
        for clave in self.DiccServer:
            time_now = self.DiccServer[clave][1]
            print(time_now)
            if time.strptime(time_now, formato) <= time.gmtime(time.time()):
                new_list.append(clave)
        for usuario in new_list:
            del self.DiccServer[usuario]

    def handle(self):

        IP = self.client_address[0]
        PORT =  self.client_address[1]
        print("IP: ", IP, "PORT: ", PORT)
        if len(self.DiccServer) == 0:
            self.json2register()
            self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n" + b"\r\n")
        while 1:

            line_bytes = self.rfile.read()
            print("El cliente nos manda: \n" + line_bytes.decode('utf-8'))
            line = line_bytes.decode('utf-8')
            if not line:
                break
            (metodo, address, sip, space, expires) = line.split()
            print(metodo)
            if metodo != "REGISTER" and not "@" in address:
                break
            time_now = int(time.time()) + int(expires)
            time_expires = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_now))
            if int(expires) == 0:
                del self.DiccServer[address]
            else:
                self.DiccServer[address] = [str(IP), str(time_expires)]
            print(self.DiccServer)
            self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n" + b"\r\n")
            self.deleteDiccServer()
            self.register2json()

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.allow_reuse_address = True
    serv.serve_forever()
    serv.close()
