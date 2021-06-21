import socket
import hashlib
from threading import Thread
import sys
import time
import os


# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
sys.setrecursionlimit(10**6)
# create the server socket
# TCP socket
s = socket.socket()
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def md5(filename):
    md5_hash = hashlib.md5()
    #filesize = os.path.getsize(filename)
    a_file = open(filename, "rb")
    content = a_file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    # close the client socket
    return digest


def merge_files(filename,list_of_files,pos):
    k = open('output_' + filename, 'ab')
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

def merge_files_2(filename,list_of_files):
    k = open('output_' + filename, 'ab')
    for x in list_of_files:
        f = open(x, 'rb')
        data = f.read()
        k.write(data)
        f.close
    k.close()
    return k

def some_function(client_socket,address,s):
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize, digest = received.split(SEPARATOR)
    filename_with_path  = 'temp\\'+str(address[1]) + '_'+filename

    # remove absolute path if there is
    #filename = os.path.basename(filename)
    filesize = int(filesize)
    files= []

    while True:
        bytes_read  = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        l = int.from_bytes(bytes_read[0:4], byteorder='big')
        f = open(filename_with_path+'_'+str(l),'wb')
        files.append(filename_with_path+'_'+str(l))
        f.write(bytes_read[4:])
        f.close()
    open('output_' + filename,'w').close()

    #merge_files(filename,files,0)
    merge_files_2(filename, files)

    client_socket.close()
    output_md5 = md5('output_'+filename)
    if(digest == output_md5):
        print(f'FILE DOWNLOADED CORRECTLY: {digest}={output_md5}')
    else:
        raise ValueError('Checksums are not correct')



while True:
    # accept connection if there is any
    client_socket, address = s.accept()
    worker = Thread(target=some_function,args=[client_socket,address,s])
    worker.start()

s.close()

