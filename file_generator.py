import os

with open('randomdata', 'wb') as f:
    f.write(os.urandom(50))