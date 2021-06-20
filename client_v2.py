import socket
import os
import hashlib

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = "192.168.1.166"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
filename = "data.csv"
# get the file size
filesize = os.path.getsize(filename)


# create the client socket
s = socket.socket()


print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

md5_hash = hashlib.md5()

a_file = open(filename, "rb")
content = a_file.read()
md5_hash.update(content)

digest = md5_hash.hexdigest()
print(digest)


# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# start sending the file
with open(filename, "rb") as f:
    start = 0
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        #print(len(bytes_read), start)
        # print(len(bytes_read))
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in
        # busy networks
        s.sendall(bytes_read)
        start+=1
# close the socket
s.close()