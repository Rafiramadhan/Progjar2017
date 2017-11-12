import socket
import sys
import threading

class Auth (threading.Thread) :
    onlinelist = {}
    flag_=True
    user = {}
    group = {}
    def __init__ (self,idthread,client,lock,conn) :
        threading.Thread.__init__(self)
        self.idthread=idthread
        self.client = client
        self.conn = conn
        self.lock = lock

    def loadUser(self):
        dict = {}

        with open('userlist.txt','r') as file:
            for line in file : #add each line to dictionary
                username, password =  line.split( )
                dict[username] = password
        file.close()
        return dict

    def loadGroup(self):
        dict = {}

        with open('grouplist.txt','r') as file:
            for line in file : #add each line to dictionary
                member = line.split(' ')
                name_group = member[0]
                del member[0]
                dict[name_group] = member
        file.close()

        return dict

  
    
    def run(self):
        print ("Melakukan koneksi ke : " + str(self.client) + " (" + self.name + ")")
        self.mainfunc()
        print ("Melakukan koneksi ke : " + str(self.client) + " (" + self.name + ")")
    
    def mainfunc(self) :
        self.user = self.loadUser()
        self.group= self.loadGroup()
        logged = 0
          
        while (1):
             ask = self.conn.recv(1024).decode()
             kata = ask.split(' ',2)
             if kata[0]== 'LOGIN' and logged == 0 :
                 self.lock.acquire()
                 if kata[1] in self.user:
                    if kata[2] == self.user[kata[1]]:
                        self.onlinelist[kata[1]]=self.conn
                        logged = 1
                        self.temp=kata[1]
                        print("\nUser "+kata[1] " Berhasil Masuk!")
                        self.conn.send(b"Berhasil")
                 self.lock.release()
             elif kata[0]== 'SIGNUP' and logged == 0 :
                 self.user[kata[1]] = kata[2]
                 self.lock.acquire()
                 file = open('userlist.txt','a')
                 toWrite = kata[1] + ' ' + kata[2] + '\n'
                 file.write(toWrite)
                 file.close()
                 print("\nBerhasil Mendaftar sebagai " + kata[1])
                 self.lock.release()
                 self.conn.send(b"berhasil")
             elif kata[0]== 'SHOWONLINE' and logged == 1 :
                 nama=self.onlinelist.keys()
                 nama2='\n'.join(nama)
                 self.conn.send(nama2.encode() + b"\n------------------")
             elif kata[0]== 'LOGOUT' and logged ==1 :
                 del self.onlinelist[self.temp]
                 self.conn.send(b"Terputus Koneksi")
                 break
             elif kata[0]== 'WHISP':
                 if kata[1] in self.user and kata[1] != self.temp :
                     try :
                         target = self.onlinelist[kata[1]]
                     except KeyError :
                         self.conn.send(b"Tidak ditemukan user yang online")
                     else :
                         msg="Private :\nPesan dari " + self.temp + " : " + kata[2]
                         target.send(msg.encode())
                         self.conn.send(b"Berhasil dikirim")
             elif kata[0]== 'BC':
                 for target in self.onlinelist.values() :
                     if target!=self.conn :
                         msg="Public : Pesan dari " + self.temp + " : " + kata[1]
                         target.send(msg.encode())
                 self.conn.send(b"Berhasil dikirim")
             elif kata[0]== 'GROUPLIST':
                if logged == 1:
                    self.lock.acquire()
                    nama = self.group.keys()
                    nama2 = '\n'.join(nama)
                    self.conn.send(nama2.encode() + b"\n------------------")
                    self.lock.release()
                    self.conn.send(b"Berhasil menampilkan")
            # elif kata[0]== 'JOINGROUP'
             #elif kata[0]== 'CHATGROUP'
             #elif kata[0]== 'LISTGROUP'
             elif kata[0]== 'MEMBERGROUP':
                 if logged ==1:
                     self.lock.acquire()
                     nama = self.group[kata[1]]
                     nama2 = '\n'.join(nama)
                     self.conn.send(nama2.encode() + b"\n------------------")
                     self.conn.send(b"\n------------------")
                     self.lock.release()
                     self.conn.send(b"Berhasil menampilkan")
            #elif kata[0]== 'LEAVEGROUP':
             else :
                self.conn.send(b"Perintah tidak dikenali")
        self.conn.close()    


        
                                                                      
        
