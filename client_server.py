import socket
import hashlib
import sys
from threading import Thread
from datetime import datetime
import os
import time
import glob


class configure_server:

    def __init__(self, host='192.168.1.153', port=5001, mode = 'server', file = 'input_files\\'+'newfile'):
        self.SERVER_HOST = str(host)
        self.SERVER_PORT = int(port)
        self.BUFFER_SIZE = 4096
        self.SEPARATOR = "<SEPARATOR>"
        self.s = socket.socket()
        if(mode == 'server'):
            self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
            self.s.listen(5)
            print(f"[*] Listening as {self.SERVER_HOST}:{self.SERVER_PORT}")
        if(mode =='client'):
            self.filename = file
            self.filesize = os.path.getsize(self.filename)
            self.s = socket.socket()
            print(f"[+] Connecting to {host}:{port}")
            self.s.connect((host, port))
            print("[+] Connected.")

class client(configure_server):

    def run(self):

        digest = hash_check.md5(self,self.filename,mode = 'client')
        print(digest)
        self.s.send(f"{self.filename}{self.SEPARATOR}{self.filesize}{self.SEPARATOR}{digest}".encode())
        with open(self.filename, "rb") as f:
            start = 0
            while True:
                bytes_read = f.read(self.BUFFER_SIZE - 4)
                k = start.to_bytes(4, byteorder='big')
                l = int.from_bytes(k, byteorder='big')
                if not bytes_read:
                    break
                time.sleep(0.1)
                self.s.send(k + bytes_read)
                start += 1
        print('SEND')
        self.s.close()

class server(configure_server):

    def accept(self):
        client_socket, address = self.s.accept()
        return client_socket, address

    def run(self, client_socket, address):
        print(f"[+] {address} is connected to the  {self.SERVER_HOST} server.")
        logs.log_to_fille(f" {address[0]} is connected to the {self.SERVER_HOST} server.\n")
        received = client_socket.recv(self.BUFFER_SIZE).decode()
        filename, filesize, self.checksum_from_client = received.split(self.SEPARATOR)
        print(filename)
        filename_with_path = 'temp\\' + str(address[1]) + '_' + filename
        self.files = []

        while True:
            bytes_read = client_socket.recv(self.BUFFER_SIZE)
            if not bytes_read:
                break
            l = int.from_bytes(bytes_read[0:4], byteorder='big')
            f = open(filename_with_path + '_' + str(l), 'wb')
            self.files.append(filename_with_path + '_' + str(l))
            f.write(bytes_read[4:])
            f.close()

        self.output_filename = 'output_files\\output_' + filename
        client_socket.close()
        open(self.output_filename, 'w').close() #cleanign output filename
        merge_files_2.merge(self) #updating output filename
        hash_check.md5(self, self.output_filename,mode = 'server')


class merge_files_2(server):
    def merge(self):
        filename = self.output_filename
        list_of_files = self.files
        k = open(filename, 'ab')
        for x in list_of_files:
            f = open(x, 'rb')
            data = f.read()
            k.write(data)
            f.close
        k.close()
        return filename


class hash_check(server,client):
    def md5(self,filename, mode):
        md5_hash = hashlib.md5()
        a_file = open(filename, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        if(mode == 'server'):
            hash_check.compare(self,digest)
        return digest

    def compare(self,digest):
        if (self.checksum_from_client == digest):
            print(f'FILE DOWNLOADED CORRECTLY: {digest} is equal to {self.checksum_from_client}')
        else:
            raise ValueError(f'Checksums are not correct.')

# class merge_files:
#     @staticmethod
#     def merge(filename,list_of_files,pos):
#         k = open(filename, 'ab')
#         f = open(list_of_files[pos], 'rb')
#         data = f.read()
#         k.write(data)
#         f.close
#         k.close()
#         if (pos< len(list_of_files)-1):
#             merge_files(filename, list_of_files, pos + 1)
#             return 0
#         else:
#             return 0

class logs:
    @staticmethod
    def log_to_fille(messange):
        now = datetime.now()
        current_time = now.strftime("%d.%m.%Y - %H:%M:%S")
        f = open('log.txt', 'a+')
        f.write(current_time + ' ' + messange)

class create_thread():
    @staticmethod
    def create(clien_socket, adress):
        serv = server()
        serv.run(clien_socket, adress)

class clean_temp_folder():
    @staticmethod
    def clean():
        files = glob.glob('temp/*')
        for f in files:
            os.remove(f)


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        if (str(sys.argv[1]) == '-s'):

            clean_temp_folder.clean() #clean temp folder

            if (len(sys.argv) == 4):
                A = server(host=str(sys.argv[2]), port=int(sys.argv[3]), mode ='server')
            else:
                A = server()
            while True:
                client_socket, address = A.accept()
                worker = Thread(target=A.run, args=[client_socket, address], daemon=True)
                worker.start()
        if (str(sys.argv[1]) == '-c'):
            print('client')
            A = client(host=str(sys.argv[2]), port=int(sys.argv[3]), mode='client', file='input_files\\'+ str(sys.argv[4]))
            A.run()
    else:
        print('No option choose, use parameters to set client (-c) or server (-s) mode')
