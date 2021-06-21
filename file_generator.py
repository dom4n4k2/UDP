import os
import random
f = open('newfile',"w+")
while os.path.getsize('newfile') <=1024*1024*4:
    k=random.randint(0,9)
    f.write(str(k))
f.close()