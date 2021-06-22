import os
import random



f = open('newfile', "a+")
f.close()
while os.path.getsize('newfile') <=1024*6:
    f = open('newfile', "a+")
    k=random.randint(0,9)
    f.write(str(k)+'\n')
    f.close



# or


# with open('randomdata', 'wb') as f:
#     f.write(os.urandom(1024*1024*1))