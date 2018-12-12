#-*-coding: utf-8-*-
from socket import *
from optparse import OptionParser as op
from cryptography.fernet import Fernet as fern
from sys import argv
from threading import *
from platform import python_version as pv
from os import system, getcwd, chdir
class Chat():
	def __init__(self, ip, port, wait, key):
		self.hashes = []
		self.f = fern(key)
		self.l = wait
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.bind((ip, port))
		self.sock.listen(self.l)
		self.sock.settimeout(0.0)
		self.clients = []
		self.t = {"wait":True,"printconn":True,"hear":True,"spy":False,"printtoken":False} 
		self.o = ("wait","printconn","hear","spy","printtoken") 
	def waitting(self):
		while self.t["wait"]:
			while len(self.clients) < self.l:
				try:
					conn, addr = self.sock.accept()
					if self.t["printconn"]:
						print(addr)
				except:
					pass
	def heartoall(self):
		while self.t["hear"]:
			for client in self.clients:
				try:
					msj = client.recv(1024)
					if self.t["spy"]:
						self.dcrypt(client, msj)
					self.sendtoall(msj, client)
				except:
					pass
	def dcrypt(self,c, token):
		try:
			t = self.f.decrypt(token)
		except:
			self.hashes.append(token)
			if self.t["printtoken"]:
				print(t)
		else:
			print(t)
	def sendtoall(self, m, c):
		for client in self.clients:
			if c == client:
				continue
			try:
				client.send(m)
			except:
				self.clients.remove(client)
def turnonoff(c, fo):
	if c in s.o:
		s.t[c] = fo
	else:
		print("Option not found.")
if __name__ == '__main__':
	opt = op("Usage: %prog [options] [data]")
	opt.add_option("-H","-i","--host",help="Set Host",type="string", dest="host", default="127.0.0.1")
	opt.add_option("-p", "--port",help="Set port", type="int", dest="port", default=5000)	
	opt.add_option("-l", "--listen",help="Set how many clients can connect at the same time.",type="int",dest="listen",default=2)
	opt.add_option("-k", "--key",help="Set Fernet key",type="string",dest="key",default="nWlbFw0M9JjS_B6AhIDR8fr0d-VtNukc5xNrYhw2vz4=")
	(o, argv) = opt.parse_args()
	o.key = o.key.encode()
	s = Chat(o.host, o.port, o.listen, o.key)
	w = Thread(target=s.waitting)
	w.daemon = True
	w.start()
	h = Thread(target=s.heartoall)
	h.daemon = True
	h.start()
	if str(pv())[0] != "3":
		raw_input = input
	cmd = ""
	while cmd != "exit":
		try:
			cmd = raw_input("{}>".format(getcwd()))
			if cmd[:2] == "cd":
				chdir(cmd[3:])
			elif cmd[:7] == "turn on":
				turnonoff(cmd[8:], True)
			elif cmd[:8] == "turn off":
				turnonoff(cmd[9:], False)