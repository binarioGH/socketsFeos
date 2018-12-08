'''
#-*-coding: utf-8-*-
from socket import *
from cryptography.fernet import Fernet as fernet
from threading import Thread
from sys import argv
from optparse import OptionParser as op
from platform import python_version as pv
from random import randint

class Server:


	def __init__(self, ip, port, usrs, key): #usrs = la cantidad de usuarios que se van a esperar
	    self.crypt = Fernet(key)

		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.bind((ip, port))
		self.sock.listen(usrs)

		
		self.users = {} #lista de usuarios

		waiting = Thread(target=self.wait, args=(usrs,))
		wating.daemon = True
		waiting.start()
		hearing = Thread(target=self.hear2all, args=())

	def wait(self, cant):
		while True:
			while len(self.users) <= cant:
				try:
					conn, addr = self.sock.accept()
					self.users.[conn] = "User-{}-{}".format(len(self.users, randint(10,1000))) 
					print("New connection/Nueva conexión: {}".format(addr))
				except Exception as e:
					print(e)

#Escuchar y procesar mensajes (abajo)/Hear, process and send messages(down)
	def hear2all(self):
		while True:
			for user in self.users:
				try:
					msj = user.recv(1024)
					msj = self.toprocess(msj, self.users[user])
					self.send2all(user, msj)

	def toprocess(self, msj, usr):
		newmsj = "{}: {}\n".format(usr,self.crypt.decrypt(msj))
		return self.crypt.encrypt(newmsj)

	def send2all(self, messenger, msj):
		for user in self.users:
			if user == messenger:
				continue
			else:
				user.send(msj)
#Escuchar, procesar y mandar mensajes (arriba)/Hear, process and send messages(up)

if __name__ == '__main__':
	#Recivir argumentos (abajo)/recive arguments (down)
	argparser = op("Uso: %prog [Opción] [Argumento]")
	argparser.add_option("-H", "--host", dest="host", type="string", help="Declarar ip del servidor./Set server's ip.")
	argparser.add_option("-p", "--port", dest="port", type="int", help="Declarar puerto./Set server's port.")
	argparser.add_option("-k", "--key", dest="key", type="string", help="Declarar la clave para encriptar (fernet)./Set cryptography key (fernet).")
	argparser.add_option("-u", "--users", dest="users", type="int", help="Declarar la cantidad de usuarios que se pueden conectar./Set how many clients can be connected to the server.")
	(o, argv) = argparser.parse_args()
	o.key = options.key.encode()
	#Recivir argumentos (arriba)/recive arguments (up)
	
	main = Server(o.host, o.port, o.users, o.key)
'''