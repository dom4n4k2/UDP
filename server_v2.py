import socket
import hashlib
from threading import Thread


# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

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


def some_function(client_socket,address,s):
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")
    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize, digest = received.split(SEPARATOR)
    filename_with_path  = 'temp\\'+str(address[1]) + '_'+filename
    print('checksum from client',digest)
    # remove absolute path if there is
    #filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    print(filesize)
    counter= 0
    print('in the loop')
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
        counter +=1

    print(files)

    k = open('output_'+filename, 'wb')
    for x in files:
        f = open(x, 'rb')
        data = f.read()
        k.write(data)
        f.close

    print('\n done')
    md5_hash = hashlib.md5()
    a_file = open('output_'+filename, "rb")
    content = a_file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    print(digest)
    # close the client socket
    client_socket.close()


while True:
    # accept connection if there is any
    client_socket, address = s.accept()
    worker = Thread(target=some_function,args=[client_socket,address,s])
    worker.start()

s.close()

