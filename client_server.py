import socket
import hashlib
import sys
from threading import Thread
from datetime import datetime
import os
import time
import glob


class configure_server:
    k = 0

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
            logs.log_to_fille(f"Server is listening as {self.SERVER_HOST}:{self.SERVER_PORT}\n")

        if(mode =='client'):
            self.filename = file
            self.filesize = os.path.getsize(self.filename)
            self.s = socket.socket()
            print(f"[+] Connecting to {host}:{port}")
            logs.log_to_fille(f"Client {self.SERVER_HOST}:{self.SERVER_PORT} is connecting to the server {host}:{port}\n")
            self.host = host
            self.port = port
            self.s.connect((self.host, self.port))
            print("[+] Connected.")
            logs.log_to_fille(
                f"Client {self.SERVER_HOST}:{self.SERVER_PORT} is CONNECTED to the server {host}:{port}\n")

class client(configure_server):

    def run(self):

        digest = hash_check.md5(self,self.filename,mode = 'client')
        logs.log_to_fille(
            f"Client {self.SERVER_HOST}:{self.SERVER_PORT} is sending file {self.filename} with size {self.filesize} and checkum md5 {digest} to the {self.host}:{self.port} server.\n")
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

        logs.log_to_fille(
            f"Client {self.SERVER_HOST}:{self.SERVER_PORT} send file {self.filename} in {start} parts.\n")
        self.s.close()

class server(configure_server):

    def accept(self):

        client_socket, address = self.s.accept()
        return client_socket, address

    def run(self, client_socket, address):

        print(f"[+] {address} is connected to the  {self.SERVER_HOST} server.")
        received = client_socket.recv(self.BUFFER_SIZE).decode()
        filename, filesize, self.checksum_from_client = received.split(self.SEPARATOR)
        filename = os.path.basename(filename)
        logs.log_to_fille(
            f"Server {self.SERVER_HOST}:{self.SERVER_PORT} try to recive file: {filename} with size {filesize}bytes and checksum md5 {self.checksum_from_client} from  {address[0]}:{address[1]} client.\n")
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

        logs.log_to_fille(
            f"Server {self.SERVER_HOST}:{self.SERVER_PORT} recived file {filename} in {l+1} parts.\n")
        self.output_filename = 'output_files\\output_' + filename
        client_socket.close()
        open(self.output_filename, 'w').close() #cleanign output filename
        merge_files_2.merge(self) #updating output filename
        hash_check.md5(self, self.output_filename,mode = 'server')

class merge_files_2(server):
    def merge(self):
        logs.log_to_fille(
            f"Server {self.SERVER_HOST}:{self.SERVER_PORT} merge recived file into {self.output_filename}.\n")
        filename = self.output_filename
        list_of_files = self.files
        k = open(filename, 'ab')
        for x in list_of_files:
            f = open(x, 'rb')
            data = f.read()
            k.write(data)
            f.close
        k.close()
        logs.log_to_fille(
            f"Server {self.SERVER_HOST}:{self.SERVER_PORT} merged recived files into {self.output_filename} with {len(list_of_files)} parts.\n")
        return filename

class hash_check(server,client):

    def md5(self,filename, mode):
        self.filename = filename
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
            logs.log_to_fille(
                f"Server {self.SERVER_HOST}:{self.SERVER_PORT} downloaded file {self.filename} from client corectly. SERVER: {digest} is equal to CLIENT: {self.checksum_from_client}\n")
        else:
            logs.log_to_fille(
                f"Server {self.SERVER_HOST}:{self.SERVER_PORT} downloaded file {self.filename} from client NOT CORECTLY. SERVER: {digest} is NOT equal to CLIENT : {self.checksum_from_client}\n")
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
        f.write(current_time + '  |||| ' + messange)

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
            logs.log_to_fille(
                f"Cleaning temp folder \n")
            if (len(sys.argv) == 4):
                A = server(host=str(sys.argv[2]), port=int(sys.argv[3]), mode ='server')
            else:
                A = server()
            while True:
                client_socket, address = A.accept()
                A.k+=1
                worker = Thread(target=A.run, args=[client_socket, address], daemon=True)
                worker.start()
                logs.log_to_fille(
                    f"Client  number {A.k} STARTS\n")
        if (str(sys.argv[1]) == '-c'):
            print('client')
            A = client(host=str(sys.argv[2]), port=int(sys.argv[3]), mode='client', file='input_files\\'+ str(sys.argv[4]))
            A.run()
    else:
        print('No option choose, use parameters to set client (-c) or server (-s) mode than if -s server_ip port or if -c server_ip port filename')
