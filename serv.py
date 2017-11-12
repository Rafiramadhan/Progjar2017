import socket
import sys 
import threading
from function import Auth

print("Menjalankan Server")
host = 'localhost'
port= 12345

sckt = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #declare socket
sckt.bind((host,port))
sckt.listen(1)

lock = threading.Lock()
tot_thread = 0
ID_thread = 1
threads = []

while (1) : #keluar masuk aktivitas server
	try:
		conn, client = sckt.accept()
		thread = Auth(ID_thread, client, lock,conn)
		thread.start()
		threads.append(thread)
		tot_thread+=1
		ID_thread+=1
	except KeyboardInterrupt :
		break

for t in threads:   #ngejoin thread yang masuk
	t.join()

print("\nMematikan Server") # keluar looping aktivitas

