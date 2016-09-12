from scipy import misc
from Crypto.Cipher import AES
import matplotlib.pyplot as plt
import binascii
import sys
import random
import rsa
from PIL import Image
import time

(public_key, private_key) = rsa.newkeys(256)

def format_data(hex_str):
    hex_str = hex_str.replace("0x",'')
    hex_str = binascii.unhexlify(hex_str)
    return hex_str
#return "\x03\x04\x05\x06\x08\x09\x70\x12\x98\x82\x34\x80\x92\x38\x40\x93"

def decrypt_hex_aes(formatted_hex):
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    decrypted_hex = obj.decrypt(formatted_hex)
    decrypted_hex = binascii.hexlify(decrypted_hex)
    rgb_arr = []
    i=0

    for x in range(16):
        rgb_arr.append(int(decrypted_hex[i:i+2] , 16))
        i+=2

    return rgb_arr

def encrypt_hex_aes(formatted_hex):
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    encrypted_hex = obj.encrypt(formatted_hex)
    encrypted_hex = binascii.hexlify(encrypted_hex)
    rgb_arr = []
    i=0

    for x in range(16):
        rgb_arr.append(int(encrypted_hex[i:i+2] , 16))
        i+=2

    return rgb_arr
def decrypt_hex_rsa(formatted_hex):
    #bob_priv = 
    global global_var 
    if global_var==0:
        global_var = 1 
        print binascii.hexlify(formatted_hex)
        print 'ft = ' , formatted_hex
    decrypted_hex = rsa.decrypt(formatted_hex,private_key)
    decrypted_hex = binascii.hexlify(decrypted_hex)
    rgb_arr = []
    i=0

    for x in range(16):
        rgb_arr.append(int(decrypted_hex[i:i+2] , 16))
        i+=2

    return rgb_arr

def encrypt_hex_rsa(formatted_hex):
    global global_var 
    encrypted_hex = rsa.encrypt(formatted_hex,public_key)
    encrypted_hex = binascii.hexlify(encrypted_hex)
    rgb_arr = []
    i=0

    for x in range(32):
        rgb_arr.append(int(encrypted_hex[i:i+2] , 16))
        i+=2

    if global_var==0:
        global_var = 1
        print binascii.hexlify(formatted_hex)
        print "Encrypted hex = " , encrypted_hex
        print 'ft = ' , formatted_hex
        print 'rgb = ' , rgb_arr
    return rgb_arr
#return [178,117,12,32,125,32,12,0,222,13,34,222,64,24,222,222,222]

def enc(dec , file_name ,enc_type):

    p_arr = [0,0,0]

    g = misc.imread(file_name)
    f = misc.imread(file_name)

    width = len(f[0])
    height = len(f)

    print width,height
    
    if (width%16)!=0:
        padding = True
        pad_length = width%16
    else:
        padding = False
        pad_length = 0
    
    rng = 16
    len_image_hex = 64
    if dec == 'e':
        width = width+pad_length
        if enc_type == 'rsa':
            rng = 32
            len_image_hex = 64
            width = 2*width
        height = height+1
        im = Image.new("RGB", (width, height))
    else:
        pad_length = f[-1][0][0]
        print f[-1]
        if enc_type == 'rsa':
            rng = 16
            len_image_hex = 128
            width = width/2
        width = width-pad_length
        height = height-1
        im = Image.new("RGB" , (width, height))
    
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
                if(len(hex_str)==len_image_hex):
                    formatted_hex = format_data(hex_str)

                    if dec=='e':
                        if enc_type=='rsa':
                            rgb = encrypt_hex_rsa(formatted_hex)
                        else:
                            rgb = encrypt_hex_aes(formatted_hex)
                    else:
                        if enc_type=='rsa':
                            rgb = decrypt_hex_rsa(formatted_hex)
                        else:
                            rgb = decrypt_hex_aes(formatted_hex)

                    for pixel in range(rng):
                        #print "In Pixel"
                        #g[i][prev_col][x] = rgb[pixel]
                        p_arr[x] = rgb[pixel]
                        x+=1
                        if x>2:
                            im.putpixel((prev_col,i),(p_arr[0],p_arr[1],p_arr[2]))
                            x%=3
                            prev_col = (prev_col+1)%(width)
                    hex_str = ''
            j+=1
        if padding==True:
            for i in range(pad_length):
                hex_val = hex(random.randrange(0,255))
                if len(str(hex_val))==3:
                    hex_val = hex_val[:2]+'0'+hex_val[2:]
                hex_str += hex_val
            
        i+=1
        j=0
        if i==height:
            print "Breaking at ",i
            break
    if dec=='e':
        for i in range (width):
            if i==0:
                im.putpixel((i,height-1),(pad_length,0,0))
            else:
                rand_num = random.randrange(0,255)
                im.putpixel((i,height-1),rand_num)

    im.save("encrypt_image.png")
    print "Saved"
    #misc.imsave("encrypted_image.png" , g)
    
    print f[0][1],"\n"
    print g[0][1],'\n'

if __name__== '__main__':
    global_var = 0
    global global_var
    t1 = time.time()
    #enc('e' , "test1.png" , 'aes')
    t2 = time.time()
    print t2-t1
    print "Ecnryption Complete"
    global_var = 0
    enc('d' , "encrypt_image.png" ,'aes')
    print time.time()-t2
