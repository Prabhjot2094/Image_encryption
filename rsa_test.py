import rsa
import binascii

(bob_pub, bob_priv) = rsa.newkeys(256)

print bob_priv , '\n' , bob_pub

message = '\x12\x34\x56\x78\x91\x23\x45\x67\x12\x12\x12\x12\x12\x12\x12\x12'

crypto = rsa.encrypt(message, bob_pub)
print len(binascii.hexlify(crypto))

message = rsa.decrypt(crypto, bob_priv)
print binascii.hexlify(message)

from scipy import misc
from Crypto.Cipher import AES
import matplotlib.pyplot as plt
import binascii
import sys
from PIL import Image


def format_data(hex_str):
    hex_str = hex_str.replace("0x",'')
    hex_str = binascii.unhexlify(hex_str)
    return hex_str
#return "\x03\x04\x05\x06\x08\x09\x70\x12\x98\x82\x34\x80\x92\x38\x40\x93"

def decrypt_hex(formatted_hex):
    #bob_priv = 
    print binascii.hexlify(formatted_hex)
    decrypted_hex = rsa.decrypt(formatted_hex,bob_priv)
    decrypted_hex = binascii.hexlify(decrypted_hex)
    rgb_arr = []
    i=0

    for x in range(16):
        rgb_arr.append(int(decrypted_hex[i:i+2] , 16))
        i+=2

    return rgb_arr

def encrypt_hex(formatted_hex):
    
    encrypted_hex = rsa.encrypt(formatted_hex,bob_pub)
    encrypted_hex = binascii.hexlify(encrypted_hex)
    rgb_arr = []
    i=0

    for x in range(16):
        rgb_arr.append(int(encrypted_hex[i:i+2] , 16))
        i+=2

    return rgb_arr
#return [178,117,12,32,125,32,12,0,222,13,34,222,64,24,222,222,222]

if __name__ == '__main__':
    g = misc.imread("jet.jpg")
    f = misc.imread("jet.jpg")
    
    hex_str = ''
    i=j=prev_col=x=0
    
    print f[0][1],"\n"
    print g[0][1],'\n'
    
    for row in f:
        for col in row:
            for ele in col:
                hex_val = hex(ele)
                if len(str(hex_val))==3:
                    hex_val = hex_val[:2]+'0'+hex_val[2:]

                hex_str += hex_val
                if(len(hex_str)==64):
                    formatted_hex = format_data(hex_str)

                    rgb = encrypt_hex(formatted_hex)

                    for pixel in range(16):
                        #print "In Pixel"
                        g[i][prev_col][x] = rgb[pixel]
                        x+=1
                        if x>2:
                            x%=3
                            prev_col = (prev_col+1)%1024
                    hex_str = ''
            j+=1
        i+=1
        j=0

    misc.imsave("encrypted_image.png" , g)
    
    print f[0][1],"\n"
    print g[0][1],'\n'



