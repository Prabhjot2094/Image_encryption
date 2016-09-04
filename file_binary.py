from Crypto.Cipher import AES

f = open('glassball.png' , 'rb')
g = open('etest2.png' , 'wb')
h = open('dtest2.png' , 'wb')


obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')

i=1
while 1:
	i+=1
	obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
	x = f.read(16)
	if len(x)!=16:
		break
	g.write(obj.encrypt(x))
g.close()

g = open('etest2.png' , 'rb')

while 1:
	i+=1
	obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
	x = g.read(16)
	if len(x)!=16:
		break
	h.write(obj.decrypt(x))





