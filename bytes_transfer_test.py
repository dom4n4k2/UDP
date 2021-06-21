filename = "randomdata"

BUFFER_SIZE = 5

with open(filename, "rb") as f:
    start = 0
    while True:

        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        #print(len(bytes_read), start)
        print('len of bytes_read', len(bytes_read))
        #print('bytes_read',bytes_read)
        k = start.to_bytes(4, byteorder='big')
        l = int.from_bytes(k, byteorder = 'big')
        print('len of start in bytes',k,start, l, len(k) )
        print('len before', len(bytes_read) , '||',bytes_read,'||' ,k)
        bytes_read = k + bytes_read
        print('len after', len(bytes_read), '||',bytes_read[0:4],'||',bytes_read[4:], '||',k , bytes_read)

        start+=1