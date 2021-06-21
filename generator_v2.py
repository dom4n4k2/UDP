import os
with open('randomdata', 'wb') as f:
    f.write(os.urandom(1024*1024*1))