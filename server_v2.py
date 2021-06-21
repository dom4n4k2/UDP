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
    filename, filesize = received.split(SEPARATOR)
    filename  = 'temp\\'+str(address[1]) + '_'+filename
    # remove absolute path if there is
    #filename = os.path.basename(filename)
    # convert to integer
    #filesize = int(filesize)
    # start receiving the file from the socket
    # and writing to the file stream
    #with open(filename, "wb") as f:
    counter= 0
    print('in the loop')
    while True:

        # read 1024 bytes from the socket (receive)
        #file_chunk = client_socket.recv(BUFFER_SIZE).decode()
        bytes_read  = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            #s.settimeout(2)
            break
        f = open(filename+ '_'+str(counter),'wb')
        # write to the file the bytes we just received
        f.write(bytes_read)
        f.close()
        ##s.sendto('ok'.encode(), address)
        counter +=1
        # update the progress bar

    print('\n done')
    md5_hash = hashlib.md5()
    a_file = open(filename+'_0', "rb")
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

