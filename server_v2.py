import socket
import hashlib
from threading import Thread
import sys
from datetime import datetime

class configure:
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5001
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    sys.setrecursionlimit(10**6)
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

class server(configure):

    def accept(self):
        client_socket, address = self.s.accept()
        return client_socket, address


def log_to_fille(messange):
    now = datetime.now()
    current_time = now.strftime("%d.%m.%Y - %H:%M:%S")
    f= open('log.txt','a+')
    f.write(current_time +' '+messange)


class hash_check():
    @staticmethod
    def md5(filename):
        md5_hash = hashlib.md5()
        #filesize = os.path.getsize(filename)
        a_file = open(filename, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        # close the client socket
        return digest



class merge_files:
    @staticmethod
    def merge(filename,list_of_files,pos):
        k = open(filename, 'ab')
        f = open(list_of_files[pos], 'rb')
        data = f.read()
        k.write(data)
        f.close
        k.close()
        if (pos< len(list_of_files)-1):
            merge_files(filename, list_of_files, pos + 1)
            return 0
        else:
            return 0

class merge_files_2:
    @staticmethod
    def merge(filename,list_of_files):
        k = open(filename, 'ab')
        for x in list_of_files:
            f = open(x, 'rb')
            data = f.read()
            k.write(data)
            f.close
        k.close()
        return k



def some_function(client_socket,address,s):
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected to the  {configure.SERVER_HOST} server.")
    log_to_fille(f" {address[0]} is connected to the {configure.SERVER_HOST} server.\n")
    # receive using client socket, not server socket
    received = client_socket.recv(configure.BUFFER_SIZE).decode()
    filename, filesize, digest = received.split(configure.SEPARATOR)
    filename_with_path  = 'temp\\'+str(address[1]) + '_'+filename

    # remove absolute path if there is
    #filename = os.path.basename(filename)
    filesize = int(filesize)
    files= []

    while True:
        bytes_read  = client_socket.recv(configure.BUFFER_SIZE)
        if not bytes_read:
            break
        l = int.from_bytes(bytes_read[0:4], byteorder='big')
        f = open(filename_with_path+'_'+str(l),'wb')
        files.append(filename_with_path+'_'+str(l))
        f.write(bytes_read[4:])
        f.close()
    output_filename = 'output_' + filename
    open(output_filename,'w').close()
    #merge_files(output_filename,files,0)

    merge_files_2.merge(output_filename, files)
    client_socket.close()
    output_md5 = hash_check.md5(output_filename)

    if(digest == output_md5):
        print(f'FILE DOWNLOADED CORRECTLY: {digest}={output_md5}')
    else:
        raise ValueError('Checksums are not correct')




server=server()


while True:
    # accept connection if there is any
    client_socket, address = server.accept()
    worker = Thread(target=some_function,args=[client_socket,address, server.s])
    worker.start()

server.s.close()

