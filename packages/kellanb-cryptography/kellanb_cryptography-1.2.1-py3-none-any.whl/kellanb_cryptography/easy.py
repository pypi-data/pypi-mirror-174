from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import ast

def encrypt(string,key):
  m = AES.MODE_GCM
  st_utf = string.encode('utf-8')
  k = (SHA256.new(data=key.encode('ascii')).hexdigest())[:32]
  k2 = bytes(k.encode('ascii'))
  cipher = AES.new(k2, m)
  ciphertext, tag = cipher.encrypt_and_digest(st_utf)
  z = [x for x in (cipher.nonce, tag, ciphertext)]
  return f"{z}"
  

def decrypt(en,key):
  m = AES.MODE_GCM
  en = ast.literal_eval(en)
  k3 = bytes(SHA256.new(data=key.encode('ascii')).hexdigest()[:32].encode('ascii'))

  tag, ciphertext = en[1],en[2]
  no = en[0]

  cipher = AES.new(k3, m, no)
  try:
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data.decode('utf-8')
  except ValueError:
    return 'bad key'
  


a = encrypt('kellan','k')
print(decrypt(a,'k'))