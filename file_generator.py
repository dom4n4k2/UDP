import os
import random
import sys

if __name__ == "__main__":
    if len(sys.argv)== 3:
        filename = str(sys.argv[1])
        print(f'cleaning {filename}')
        f = open(filename, "a+")
        f.close()
        print('BUILDING FILE IN PROGRESS')
        while os.path.getsize(filename) <=int(sys.argv[2]):
            f = open(filename, "a+")
            k=random.randint(0,9)
            f.write(str(k)+'\n')
            f.close
        print('file done')

    else:
        print('insert filename and size of file in bytes -- python file_generator.py filename 1024')





# or


# with open('randomdata', 'wb') as f:
#     f.write(os.urandom(1024*1024*1))