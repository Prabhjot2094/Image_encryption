import json
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Cipher import DES
import pyDes
import rsa
import time
import sys
import binascii
import math
import os
import md5

def get_hash(password):
    md = md5.new()
    md.update(password)
    md = md.digest()
    hash_hex = binascii.hexlify(md)
    return hash_hex[:16]

def format_data(hex_str):
    #print hex_str
    hex_str = hex_str.replace("0x",'')
    hex_str = binascii.unhexlify(hex_str)
    return hex_str

def calc_dim(file_size , enc_type):

    if enc_type=='rsa':
        file_size = file_size*32/21
    added_bytes = file_size%3
    t1 = file_size/3.0
    t2 = pow(t1,0.5)
    t3 = int(t2)

    print "shortage = ", added_bytes
    if t2-t3!=0:
        x = t3+2
        y = t3+1
    else:
        x=y=int(t2)
    return x,y

def calc_dim_rsa(file_size):
    file_size = file_size*no_of_rgbs/bytes_to_read
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

def get_img_ext(height , im):
    ext_len,e1,e2 = im.getpixel((2,height-1))
    ext_str = hex(e1)[2:]+hex(e2)[2:]
    i=0
    j=3
    while 1:
        rgb = im.getpixel((j,height-1))
        i+=3
        if i>ext_len-2:
            diff = i-ext_len+2
            print "diff = " , diff
            for val in range(diff+1):
                print "val = ",val
                h = hex(rgb[val])[2:]
                if len(h)==1:
                    h ='0'+h
                ext_str+=h 
            break
        else:
            for t in range(3):
                h = hex(rgb[t])[2:]
                if len(h)==1:
                    h ='0'+h
                ext_str+=h
        j+=1
    ext = binascii.unhexlify(ext_str)
    return ext

def enc(enc_type , file_name , key=''):
    #sys.exit(10)
    if enc_type=='rsa':
        (public_key, private_key) = rsa.newkeys(256 , poolsize=2)
        priv_key = str(private_key.n)+'@'+str(private_key.e)+'@'+str(private_key.d)+'@'+str(private_key.p)+'@'+str(private_key.q)
        bytes_to_read = 21
        no_of_rgbs = 32
    elif enc_type=='aes' or enc_type=='des':
        if enc_type=='des':
            obj = DES.new(key[:8], DES.MODE_CBC,'\0\0\0\0\0\0\0\0')
        bytes_to_read = 16
        no_of_rgbs = 16

    f_name , ext = os.path.splitext(file_name)
    file_size = os.path.getsize(file_name)
    width,height = calc_dim(file_size , enc_type)

    print width,height
    height+=1
    #sys.exit() 
    im = Image.new("RGB" , (width, height))
    f = open(file_name , 'rb')

    final_bytes = False
    i=j=prev_col=x=0
    p_arr=[0,0,0]
    padding = '123456789101312'

    s=0
    while 1:
        s+=1
       # print s
        ''' i+=1
        if i>bytes_to_read3:
            i=i%bytes_to_read3
            j+=1
        '''
        #print j,i

        z = f.read(bytes_to_read)
        if len(z)!=bytes_to_read:
            #print len(z)
            t1 = bytes_to_read-len(z)
            extra_bytes = len(z)
            z+=padding[:t1]
            final_bytes = True
        
        if s==1 or s==2 or s==3:
            print "Hex just before encryption = ",binascii.hexlify(z)

        if enc_type=='aes':
            obj = AES.new(key, AES.MODE_CBC, 'This is an IV456')
            encrypted_hex = obj.encrypt(z)
        elif enc_type=='rsa':
            encrypted_hex = rsa.encrypt(z,public_key)
        elif enc_type=='des':
            encrypted_hex = obj.encrypt(z)
        
        encrypted_hex = binascii.hexlify(encrypted_hex)
        
        if s==1 or s==2 or s==3 or final_bytes==True:
            print "Hex after encryption = ",encrypted_hex
            print "Hex length after encryption = ",len(encrypted_hex)

        rgb_arr = []

        t=0

        for d in range(no_of_rgbs):
            rgb_arr.append(int(encrypted_hex[t:t+2] , 16))
            t+=2
        for pixel in range(no_of_rgbs):
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
            if p_arr!=[0,0,0]:
                im.putpixel((prev_col,j),(p_arr[0],p_arr[1],p_arr[2]))
            break
    
    t2 = prev_col/256
    t3 = prev_col%256
    im.putpixel((0,height-1),(t2,t3,extra_bytes))
    
    t1 = last_pixel_row/256
    t2 = last_pixel_row%256
    im.putpixel((1,height-1),(t1,t2,0))
    
    ext_len = len(ext)
    ext = binascii.hexlify(ext)
    print "Ext = ",ext

    i=x=0
    count=1
    prev_col = 2
    p_arr[0] = ext_len
    x+=1
    while count<=ext_len:
            print i,count , x
            count+=1
            p_arr[x] = int(ext[i:i+2],16)
            i+=2
            x+=1
            if x>2:
                print p_arr,i
                im.putpixel((prev_col,height-1),(p_arr[0],p_arr[1],p_arr[2]))
                x%=3
                prev_col = (prev_col+1)
                prev_col%=width
                p_arr = [0,0,0]
   
    if p_arr!=[0,0,0]:
            print p_arr
            im.putpixel((prev_col,height-1),(p_arr[0],p_arr[1],p_arr[2]))
            prev_col+=1
    f.close() 
    for i in range(prev_col,width):
            im.putpixel((i,height-1),(255,1,231))
    im.save(f_name+".png")
    if enc_type=='rsa':
		return priv_key
    

def dec(enc_type , enc_file_name , dec_file_name , key):
    if enc_type=='rsa':
        key = key.replace(", ","@")
        print len(key)
        #sys.exit()
        key = key.split("@")
        private_key = rsa.PrivateKey(int(key[0]),int(key[1]),int(key[2]),int(key[3]),int(key[4]))
    print enc_file_name
    im = Image.open(enc_file_name)
    width,height = im.size
    ext = get_img_ext(height , im)

    dec_file_name += ext
    print dec_file_name
    f = open(dec_file_name,'wb')
    
    if enc_type=='rsa':
        bytes_to_read = 21
        no_of_rgbs = 32
    elif enc_type=='aes' or enc_type=='des':
        if enc_type == 'des':
            obj = DES.new(key[:8], DES.MODE_CBC,'\0\0\0\0\0\0\0\0')
        bytes_to_read = 16
        no_of_rgbs = 16

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

        if x>no_of_rgbs:
            for z in range(no_of_rgbs):
                hex_val = hex(rgb_arr.pop(0))
                if len(str(hex_val))==3:
                    if i==t4 and j==k3:
                        print hex_val
                    hex_val = hex_val[:2]+'0'+hex_val[2:]
                hex_str += hex_val 
            
            x%=no_of_rgbs
            hex_str = format_data(hex_str)
            
            if d==0 or d==1 or d==2 or (i==t4 and j==k3):
                print "hex before decryption = ", binascii.hexlify(hex_str)
                print "hex length before decryption = ", len(binascii.hexlify(hex_str))
            
            if enc_type=='aes':
                obj = AES.new(key, AES.MODE_CBC, 'This is an IV456')
                decrypted_hex = obj.decrypt(hex_str)
            elif enc_type=='rsa':
                try:
                    decrypted_hex = rsa.decrypt(hex_str,private_key)
                except:
                    print "Wrong Key Entered !!!!!"
                    sys.exit()
            elif enc_type=='des':
                decrypted_hex = obj.decrypt(hex_str)
            
            if i==t4 and j==k3:
                f.write(decrypted_hex[:t3])
                print "Breaking at ", i, j
                break
            if d==0 or d==1 or d==2:
                d+=1
                print "hex rigth after decryption = ", binascii.hexlify(decrypted_hex)
            f.write(decrypted_hex[:bytes_to_read])
            hex_str = ''
        i+=1
        if i>=width:
            i%=width
            j+=1
    f.close()
    return dec_file_name

def encrypt(file_name,keys,toggle_list):
	try:
		enc_type = ["des","rsa","aes"]

		keys[0] = get_hash(keys[0]) 
		keys[2] = get_hash(keys[2]) 
		
		f_name = file_name.split('.')

		cnt = toggle_list.count(1)

		t1=time.time()
		if cnt==1:
			pos = toggle_list.index(1)
			t1=time.time()
			rsa = enc(enc_type[pos] , file_name , keys[pos])
			t2=time.time()
			time_taken=[t2-t1,t2-t1]
		elif cnt==2:
			pos = [i for i, x in enumerate(toggle_list) if x == 1]
			print keys[pos[1]],keys[pos[0]]
			print enc_type[pos[0]],enc_type[pos[1]]
			t1=time.time()
			r1 = enc(enc_type[pos[0]] , file_name ,keys[pos[0]])
			t2=time.time()
			r2 = enc(enc_type[pos[1]] , f_name[0]+'.png' , keys[pos[1]])
			t3=time.time()
			
			if pos[1]==1:
				rsa=r1
			elif pos[0]==1:
				rsa=r2
			time_taken=[t2-t1,t3-t2,t3-t1]
		elif cnt==3:
			pos = [0,1,2]
			t1=time.time()
			enc(enc_type[pos[0]] , file_name ,keys[pos[0]])
			t2=time.time()
			rsa = enc(enc_type[pos[1]] , f_name[0]+'.png' , keys[pos[1]])
			t3=time.time()
			enc(enc_type[pos[2]] , f_name[0]+'.png' , keys[pos[2]])
			t4=time.time()
			
			time_taken=[t2-t1,t3-t2,t4-t3,t4-t1]
		print rsa
		return [rsa,1,time_taken]
	except Exception as e:
		return [e[0],0]
def decrypt(file_name,keys,toggle_list):
	try:
		enc_type = ["des","rsa","aes"]

		keys[0] = get_hash(keys[0]) 
		keys[2] = get_hash(keys[2]) 
		
		f_name = file_name.split('.')

		cnt = toggle_list.count(1)

		
		if cnt==1:
			pos = toggle_list.index(1)
			t1=time.time()
			dec_file_name = dec(enc_type[pos] , file_name, f_name[0] , keys[pos])
			t2=time.time()

			time_taken = [t2-t1,t2-t1]
		elif cnt==2:
			pos = [i for i, x in enumerate(toggle_list) if x == 1]
			print keys[pos[1]],keys[pos[0]]
			print enc_type[pos[1]],enc_type[pos[0]]	
			
			t1=time.time()
			dec(enc_type[pos[1]] , file_name ,"temp1"  , keys[pos[1]])
			t2=time.time()
			dec_file_name = dec(enc_type[pos[0]] , "temp1.png", f_name[0] , keys[pos[0]])
			t3=time.time()

                        os.remove("temp1.png")
			time_taken=[t2-t1,t3-t2,t3-t1]
		elif cnt==3:
			pos = [0,1,2]
			t1=time.time()
			dec(enc_type[pos[2]] ,file_name ,"temp1", keys[2])
			t2=time.time()
			dec(enc_type[pos[1]] ,"temp1.png","temp2" , keys[1])
			t3=time.time()
			dec_file_name =dec(enc_type[pos[0]] ,"temp2.png", f_name[0], keys[0])
			t4=time.time()
			
			os.remove("temp1.png")
			os.remove("temp2.png")
			time_taken=[t2-t1,t3-t2,t4-t3,t4-t1]
		return [dec_file_name,1,time_taken]
	except Exception as e:
		rsa_error = "invalid literal for"
		temp = rsa_error in str(e)
		
		if temp == True:
			return ["Invalid Private key for RSA !!",0]
		else:
			return [e[0],0]
def main(argv):
	argv = argv[0].split('#')
	print argv[0]
	print str(argv)

	for i in range(2,4):
		print i,argv[i]
		argv[i]=json.loads(argv[i])
	if argv[0]=="encrypt":
		encrypt(argv[1],argv[2],argv[3])
	elif argv[0]=="decrypt":
		file_name = decrypt(argv[1],argv[2],argv[3])
		return file_name


if __name__=='__main__':
	if sys.argv[1:]:
		main(sys.argv[1:])
	"""t1 = time.time()
	password = get_hash("password")
	enc('aes' ,'test1.png' , password)
	enc('des' ,'test1.png' , password)
	dec('des' ,'test1.png' ,'face1' , password)
	dec('aes' ,'face1.png' ,'fac2' , password)
	enc_dec = raw_input('Enter\ne : Encryption\nd : Decryption\n')

    priv_key = ''
    if enc_dec=='e':
        file_name = raw_input('Enter the file name\n')
        enc_type = raw_input('Enter the Type of Encryption: aes , des , rsa\n')
        if enc_type!='rsa':
            priv_key = raw_input('Enter the desired  encrytion key : \n')
            priv_key = get_hash(priv_key)
        enc(enc_type , file_name , priv_key)

    elif enc_dec=='d':
        file_name = raw_input('Enter the file name\n')
        enc_type = raw_input('Enter encryption applied on the image: aes , des , rsa\n')
        priv_key = raw_input('Enter the key : \n')

        if enc_type!='rsa':
            priv_key = get_hash(priv_key)
        f_name = file_name.split('.')[0]
        dec(enc_type , file_name , f_name , priv_key)
    sys.exit()"""
