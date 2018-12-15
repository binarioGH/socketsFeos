'''
#-*-coding: utf-8-*-
from socket import *
from optparse import OptionParser as op
from os import system, chdir, getcwd
from threading import Thread 
from cryptography.fernet import Fernet as fern 
from platform import python_version as pv
from sys import argv
class Server():
	def __init__(self,ip,port,listen, key):
		self.f = fern(key)
		self.l = listen
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.bind((ip, port))
		self.sock.listen(self.l)
		self.sock.settimeout(0.0)
		self.clients = []
		self.cmd = {"waitting":True,"printaddr":True,"hearing":True,"spy":False,"printtoken":True,"savehash":True}
		self.verifycmd = ("waitting","printaddr","hearing","spy","printtoken","savehash")
		self.hashes = []
		w = Thread(target=self.wat)
		w.daemon = True
		w.start()
		h = Thread(target=self.hear)
		h.daemon = True
		h.start()
	def wait(self):
		while self.cmd["waitting"]:
			while len(self.clients) < self.l:
				try:
					conn, addr = self.sock.accept()
					if self.cmd["printaddr"]:
						print("\nNew connection:\nip:{}\nport:{}\n".format(addr[0],addr[1]))
                    self.clients.append(conn)
                except:
                    pass
    def hear(self):
        while self.cmd["hearing"]:
            for client in self.clients:
                try:
                	msj = client.recv(1024)
                	if self.cmd["spy"]:
                		self.dcrpt(msj)
                	self.send2all(client, msj)
                except:
                	pass
    def dcrpt(self, m):
    	try:
    		token = f.decrypt(m)
    	except:
    	    if self.cmd["printtoken"]:
    	        print(m.decode())
    	    if self.cmd["savehash"]:
    	    	self.hashes.append(msj.decode())
    	else:
    	    print(token.decode())
    def send2all(self, c, m):
        for cl in self.clients:
        	try:
        		if cl == c:
        			continue
        		else:
        			cl.send(m)
        	except:
        		self.clients.remove(cl)

if __name__ == '__main__':
	opt = op("Usage: %prog [option] [value]")
	opt.add_option("-H", "--host",dest="ip",help="Set server's ip",default="127.0.0.1",type="string")
	opt.add_option("-p","--port",dest="port",help="Set server's port",default=5000,type="int")
	opt.add_option("-l","--listen",dest="listen",help="Set how many clients can be connected to the server at the same time",default=2,type="int")
	opt.add_option("-k","--key",dest="key",help="Set Fernet's key",default="nWlbFw0M9JjS_B6AhIDR8fr0d-VtNukc5xNrYhw2vz4=",type="string")
    (o, argv) = opt.parse_args()
    o.key = o.key.encode()
	s = Server(o.ip, o.port, o.listen, o.key)
	if str(pv())[0] == "3":
		raw_input = input
	cmd = ""
	while cmd != "exit":
		pass
'''

'''
    Quiero hacer un servidor donde se puedan subir y bajar archivos uwu
'''