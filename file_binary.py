from PIL import Image
from Crypto.Cipher import AES
import rsa
import sys
import binascii
import math
import os

def format_data(hex_str):
    #print hex_str
    hex_str = hex_str.replace("0x",'')
    hex_str = binascii.unhexlify(hex_str)
    return hex_str

def calc_dim(file_size):
    added_bytes = file_size%3
    t1 = file_size/3
    t2 = pow(t1,0.5)
    t3 = int(t2)

    print "shortage = ", added_bytes
    if t2-t3!=0:
        x = t3+2
        y = t3+1
    else:
        x=y=t2
    return x,y

def enc():
    file_name = 'test4.jpg' 
    file_size = os.path.getsize(file_name)
    width,height = calc_dim(file_size)

    print width,height
    height+=1
    #sys.exit() 
    im = Image.new("RGB" , (width, height))
    f = open(file_name , 'rb')

    final_bytes = False
    i=j=prev_col=x=0
    p_arr=[0,0,0]
    enc_type = 'aes'
    padding = '123456789101312'

    s=0
    while 1:
        s+=1
       # print s
        ''' i+=1
        if i>213:
            i=i%213
            j+=1
        '''
        #print j,i

        z = f.read(16)
        if len(z)!=16:
            #print len(z)
            t1 = 16-len(z)
            extra_bytes = len(z)
            z+=padding[:t1]
            final_bytes = True
        if enc_type=='rsa':
            g.write(rsa.encrypt(z,priv))
        else:
            if s==1 or s==2 or s==3:
                print "Hex just before encryption = ",binascii.hexlify(z)
            obj = AES.new('aaaaaaaaaaaaaaaa', AES.MODE_CBC, 'This is an IV456')
            encrypted_hex = obj.encrypt(z)
            encrypted_hex = binascii.hexlify(encrypted_hex)
            if s==1 or s==2 or s==3:
                print "Hex after encryption = ",encrypted_hex

            rgb_arr = []

            t=0
    
            for d in range(16):
                rgb_arr.append(int(encrypted_hex[t:t+2] , 16))
                t+=2
            for pixel in range(16):
                        p_arr[x] = rgb_arr[pixel]
                        x+=1
                        if final_bytes==True:
                            if pixel==t1:
                                rgb_pos = x-1
                                last_pixel_col = prev_col
                                last_pixel_row = j
                                print last_pixel_row
                        if x>2:
                            im.putpixel((prev_col,j),(p_arr[0],p_arr[1],p_arr[2]))
                            x%=3
                            prev_col = (prev_col+1)
                            i=prev_col
                            if prev_col>width-1:
                                j+=1
                            prev_col%=width
                            p_arr = [0,0,0]
        if final_bytes==True:
            print p_arr
            break
    t2 = prev_col/256
    t3 = prev_col%256
    im.putpixel((0,height-1),(t2,t3,extra_bytes))
    t1 = last_pixel_row/256
    t2 = last_pixel_row%256
    im.putpixel((1,height-1),(t1,t2,0))
    
    for i in range(2,width):
            im.putpixel((i,height-1),(255,1,231))
    im.save("file_image.png")

def dec():
    im = Image.open("file_image.png")
    f = open("decrypted_image.jpg",'wb')
    width,height = im.size
    

    t1,t2,t3 = im.getpixel((0,height-1))
    k1,k2 = im.getpixel((1,height-1))[:2]

    t4 = (t1*256)+t2
    k3 = (k1*256)+k2
    
    print t1,t2,t3,k3
   
    i=j=x=d=0
    hex_str = ''
    rgb_arr = []
    while 1:
        try:
            r,g,b = im.getpixel((i,j))
        except:
            print i,j
            sys.exit()

        rgb_arr.append(r)
        rgb_arr.append(g)
        rgb_arr.append(b)
        x+=3

        if x>16:
            for z in range(16):
                hex_val = hex(rgb_arr.pop(0))
                if len(str(hex_val))==3:
                    hex_val = hex_val[:2]+'0'+hex_val[2:]
                hex_str += hex_val 
            x%=16
            hex_str = format_data(hex_str)
            #hex_str = binascii.hexlify(hex_str)
            #rint binascii.hexlify(hex_str)
            #hex_str = binascii.unhexlify(hex_str)
            if d==0 or d==1 or d==2:
                print "hex before decryption = ", binascii.hexlify(hex_str)
            obj = AES.new('aaaaaaaaaaaaaaaa', AES.MODE_CBC, 'This is an IV456')
            decrypted_hex = obj.decrypt(hex_str)
            if i==t4 and j==k3:
                f.write(decrypted_hex[:t3])
                print "Breaking at ", i, j
                break
            if d==0 or d==1 or d==2:
                d+=1
                print "hex rigth after decryption = ", binascii.hexlify(decrypted_hex)
            f.write(decrypted_hex)
            hex_str = ''
        i+=1
        if i>=width:
            i%=width
            j+=1
    f.close()











enc()
dec()
sys.exit()
'''
f = open('glassball.png' , 'rb')
g = open('etest2.png' , 'wb')
h = open('dtest2.png' , 'wb')

im1 = Image.new("RGB" , (213, 213))
im2 = Image.new("RGB" , (213, 213))

(pub,priv) = rsa.newkeys(256)

obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')

i=j=prev_col=x=0
p_arr=[0,0,0]
enc_type = 'aes'

s=0
while 1:
        s+=1
       # print s
         i+=1
        if i>213:
            i=i%213
            j+=1
        
        #print j,i

        obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
        z = f.read(16)
        if len(z)!=16:
            pass
        if enc_type=='rsa':
            g.write(rsa.encrypt(z,priv))
        else:
            encrypted_hex = obj.encrypt(z)
            if s==1:
                print "Hex after encryption = ",encrypted_hex
            encrypted_hex = binascii.hexlify(encrypted_hex)
            rgb_arr = []

            t=0
    
            for d in range(16):
                rgb_arr.append(int(encrypted_hex[t:t+2] , 16))
                t+=2
            for pixel in range(16):
                        p_arr[x] = rgb_arr[pixel]
                        x+=1
                        if x>2:
                            im1.putpixel((prev_col,j),(p_arr[0],p_arr[1],p_arr[2]))
                            x%=3
                            prev_col = (prev_col+1)
                            i=prev_col
                            if prev_col>212:
                                j+=1
                            prev_col%=213

            
print i
g.close()
im1.save("file_image.png")

i=j=x=d=0
rgb_arr = []
hex_str=''
im = Image.open("file_image.png")
f = open("decrypted_image.png" , 'wb')
for t in range(213*213):
        #print i,j
        if i>212:
            i%=213
            j+=1

        r,g,b = im.getpixel((i,j))
        x+=3

        rgb_arr.append(r)
        rgb_arr.append(g)
        rgb_arr.append(b)

        if x>16:
            for z in range(16):
                hex_val = hex(rgb_arr.pop(0))
                if len(str(hex_val))==3:
                    hex_val = hex_val[:2]+'0'+hex_val[2:]
                hex_str += hex_val 
            x%=16
            hex_str = format_data(hex_str)
            if d==0:
                d=1
                print "hex before decryption = ", hex_str
            decrypted_hex = obj.decrypt(hex_str)
            f.write(decrypted_hex)
            hex_str = ''
        i+=1
f.close()         
            
'''
        




