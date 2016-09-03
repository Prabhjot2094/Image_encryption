from scipy import misc
from Crypto.Cipher import AES
import matplotlib.pyplot as plt
import binascii
import sys
from PIL import Image

img = Image.open("test2.jpg") # create a new black image
pixels = img.load() # create the pixel map )
print pixels[0,1]

sys.exit()

g = misc.face()#imread("face.png")
f = misc.imread("test1.png")

#misc.imsave('face.png',f)


def format_data(hex_str):
    #print hex_str
    hex_str = hex_str.replace("0x",'')
    #print hex_str
    hex_str = binascii.unhexlify(hex_str)
    #print hex_str
    return hex_str
    #return "\x03\x04\x05\x06\x08\x09\x70\x12\x98\x82\x34\x80\x92\x38\x40\x93"

def encrypt_hex(formatted_hex):
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    obj1 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    
    encrypted_hex = obj.encrypt(formatted_hex)
   # encrypted_hex = obj1.decrypt(encrypted_hex)
    encrypted_hex = binascii.hexlify(encrypted_hex)

    rgb_arr = []
    i=0

    for x in range(16):
        rgb_arr.append(int(encrypted_hex[i:i+2] , 16))
        i+=2

    return rgb_arr
    
    #return [178,117,12,32,125,32,12,0,222,13,34,222,64,24,222,222,222]


hex_str = ''
i=j=prev_col=x=0


plt.imshow(f)
misc.imsave("encrypted_image.png" , f)

print f[0],"\n"
print g[0]
sys.exit()

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

print i,j,prev_col

f[616][463] = [256,0,0]
print g[0][1]

misc.imsave("encrypted_image.png" , g)

plt.imshow(g)
plt.show()
