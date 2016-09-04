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
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    decrypted_hex = obj.decrypt(formatted_hex)
    decrypted_hex = binascii.hexlify(decrypted_hex)
    rgb_arr = []
    i=0

    for x in range(16):
        rgb_arr.append(int(decrypted_hex[i:i+2] , 16))
        i+=2

    return rgb_arr

def encrypt_hex(formatted_hex):
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    encrypted_hex = obj.encrypt(formatted_hex)
    encrypted_hex = binascii.hexlify(encrypted_hex)
    rgb_arr = []
    i=0

    for x in range(16):
        rgb_arr.append(int(encrypted_hex[i:i+2] , 16))
        i+=2

    return rgb_arr
#return [178,117,12,32,125,32,12,0,222,13,34,222,64,24,222,222,222]

if __name__ == '__main__':
    g = misc.imread("encrypted_image.png")
    f = misc.imread("encrypted_image.png")
    
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

                    rgb = decrypt_hex(formatted_hex)

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


'''im = Image.new("RGB",(1024,768),"white")

i=j=0
for row in g:
        j=0
        for col in row:
                li = (col[0],col[1],col[2])
                im.putpixel((j,i),li)
                j+=1
        i+=1

im.save('epil_save.jpg')

im.save("epil_save.jpg", "JPEG", quality=100)
#x = misc.imread("epil_save.jpg")

#print "Jpeg: " , f[0][1],'\n',"Jpeg: ",x[0][1] #, '\n' , "PNG: ",h[0][1]'''
