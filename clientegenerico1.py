#-*-coding: utf-8-*-
from socket import * 
from threading import Thread
from cryptography.fernet import Fernet as fern
from optparse import OptionParser as op
from sys import argv
from platform import python_version as pv, platform as p
from os import system
def sendmsj(m):
	try:
		sock.send(f.encrypt(m.encode()))
	except Exception as e:
		print(e)
def hearing():
	print("Hearing...")
	while True:
		try:
			msj = f.decrypt(sock.recv(1024)).decode()
			print("\n{}\n>>>".format(msj))
		except Exception as e:
			print(e)
if __name__ == '__main__':
	opt = op("usage: %prog [options] [values]")
	opt.add_option("-H","--host",dest="ip",type="string",help="Set server's ip",default="127.0.0.1")
	opt.add_option("-p","--port",dest="port",type="int",help="Set server's port",default=5000)
	opt.add_option("-k","--key",dest="key",type="string",help="Set chat's Fernet key",default="nWlbFw0M9JjS_B6AhIDR8fr0d-VtNukc5xNrYhw2vz4=")
	(o, argv) = opt.parse_args()
	f = fern(o.key)
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((o.ip, o.port))
	h = Thread(target=hearing)
	h.daemon = True
	h.start()
	if str(pv())[0] == "3":
		raw_input = input
	if str(p())[0].lower() == "w":
		clear = "cls"
	else:
		clear = "clear"
	cmd = ""
	costum_clear = clear
	print("Type 'exit' to quit.")
	while cmd != "exit":
		try:
			cmd = raw_input(">>>")
			if cmd[:9] == "SET CLEAR":
				costum_clear = cmd[10:]
			elif cmd == costum_clear:
				system(clear)
			else:
				sendmsj(cmd)
		except Exception as e:
			print(e)