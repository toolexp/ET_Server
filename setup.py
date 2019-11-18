import hashlib

new = 'hoalalalala'
print(hashlib.sha1(new.encode()).hexdigest())