import socket
import sys 
import threading

print("Menjalankan Client")
host = 'localhost'
port= 12345

sckt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:	#try to connect to server
	sckt.connect((host,port))
except socket.error as msg:	
	sckt.close()
	print("Tidak terhubung ke server")
	sys.exit(1)
if sckt is not None:
	while True:
		data = input()
		if data.lstrip() != '' :
			sckt.send(data.encode())	#encode the user message so it can be send with sock.send()
			incoming = sckt.recv(2048).decode()	#decode incoming message from server
			if incoming == "Terputus Koneksi":	#if server close connection,close socket on client too
				print("Koneksi Selesai")
				sckt.close()
				break
			print(incoming)	#print server message
	sys.exit(1)

