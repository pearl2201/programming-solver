import requests
import os
os.system('clear')

uri = 'http://challenge01.root-me.org/programmation/ch1/'
s = requests.Session()
r = s.get(uri)
def cal(a,b,u0,n, isAdd):
	u_ret = []
	u_t = u0
	for i in range(n):
		if isAdd:
			u_t = (a + u_t) + (i*b)
		else:
			u_t = (a + u_t) - (i*b)
		u_ret.append(u_t)
	print (u_ret[0:3])
	print (u_ret[-3:])

	return u_t
	
a1 = int(r.text[r.text.find('= [')+3:r.text.find(' + U<sub>n')])
a2 = int(r.text[r.text.find('[ n *')+6:r.text.find(' ]<br />\nU')])
u0 = int(r.text[r.text.find('0</sub> =')+10:r.text.find('\n<br />You')])
n = int(r.text[r.text.find('find U<sub>')+11:r.text.find('</sub><br /><br />')])
isAdd = r.text[r.text.find('n</sub> ] ')+10:r.text.find('n</sub> ] ')+11] == '+'

print ("html: %s" %r.text)
print ("parse: a1: %d - a2: %d - u0: %d - n: %d - isAdd: %s" %(a1,a2,u0,n,str(isAdd)))
result = cal(a1,a2,u0,n,isAdd)
print ('result %d' %result)
uri_result = 'http://challenge01.root-me.org/programmation/ch1/ep1_v.php?result=%d' %result
print (uri_result)
r = s.get(uri_result)
print (r.text)



