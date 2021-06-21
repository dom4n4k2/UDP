import hashlib
filename = 'randomdata'
md5_hash = hashlib.md5()
a_file = open(filename, "rb")
content = a_file.read()
md5_hash.update(content)
digest = md5_hash.hexdigest()
print(digest)



filename = 'output_randomdata'
md5_hash = hashlib.md5()

a_file = open(filename, "rb")
content = a_file.read()
md5_hash.update(content)
digest = md5_hash.hexdigest()
print(digest)
