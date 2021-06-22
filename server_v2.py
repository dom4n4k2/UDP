import socket
import hashlib
import sys
from threading import Thread
from datetime import datetime


class configure_server:
    def __init__(self, host='0.0.0.0', port=5001):
        self.SERVER_HOST = str(host)
        self.SERVER_PORT = int(port)
        self.BUFFER_SIZE = 4096
        self.SEPARATOR = "<SEPARATOR>"
        self.s = socket.socket()
        print(self.SERVER_HOST, self.SERVER_PORT)
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.s.listen(5)
        print(f"[*] Listening as {self.SERVER_HOST}:{self.SERVER_PORT}")


class server(configure_server):

    def accept(self):
        client_socket, address = self.s.accept()
        return client_socket, address

    def run(self, client_socket, address):
        print(f"[+] {address} is connected to the  {self.SERVER_HOST} server.")
        logs.log_to_fille(f" {address[0]} is connected to the {self.SERVER_HOST} server.\n")
        received = client_socket.recv(self.BUFFER_SIZE).decode()
        filename, filesize, self.checksum_from_client = received.split(self.SEPARATOR)
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

        self.output_filename = 'output_' + filename
        open(self.output_filename, 'w').close()
        client_socket.close()
        merge_files_2.merge(self)
        hash_check.md5(self)


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
        return k


class hash_check(merge_files_2):
    def md5(self):
        md5_hash = hashlib.md5()
        a_file = open(self.output_filename, "rb")
        content = a_file.read()
        md5_hash.update(content)
        self.digest = md5_hash.hexdigest()
        hash_check.compare(self)
        return

    def compare(self):
        if (self.checksum_from_client == self.digest):
            print(f'FILE DOWNLOADED CORRECTLY: {self.digest} is equal to {self.checksum_from_client}')
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


if __name__ == "__main__":



    if (len(sys.argv) > 1):
        if (str(sys.argv[1]) == '-s'):
            if (len(sys.argv) == 4):
                A = server(host=str(sys.argv[2]), port=int(sys.argv[3]))
            else:
                A = server()
            while True:
                client_socket, address = A.accept()
                worker = Thread(target=A.run, args=[client_socket, address], daemon=True)
                worker.start()

        if (str(sys.argv[1]) == '-c'):
            print('client')
    else:
        print('No option choose, use parameters to set client (-c) or server (-s) mode')
