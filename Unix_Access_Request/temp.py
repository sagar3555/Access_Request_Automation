
def Encode () :


    sample_pass = 'sample_password'.rjust(32)
    secret_key = '1234567890123456'  # create new & store somewhere safe

    cipher = AES.new(secret_key, AES.MODE_ECB)  # never use ECB in strong systems obviously
    encoded = base64.b64encode(cipher.encrypt(sample_pass))
    print (encoded)


    # ...
    decoded = cipher.decrypt(base64.b64decode(encoded))
    print (decoded.strip())

#Encode()

from Crypto.Cipher import AES
import base64
secret_key = '1234567890123456'
cipher = AES.new(secret_key, AES.MODE_ECB)
encoded_sample_password  = "gUhd9TxpnQppnZVAf7cv9g/iIbQKwmYTG8L7R5hOx58="

password = cipher.decrypt(base64.b64decode(encoded_sample_password))
print (password.strip())
