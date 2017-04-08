import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION

from nssrc.com.citrix.netscaler.nitro.resource.config.basic.service import service as NSSVC
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcipher import sslcipher as SSLCIPHER
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice import sslservice as SSLSVC
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslciphersuite import sslciphersuite as SSLCIPHERSUITE

import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver
import nssrc.com.citrix.netscaler.nitro.service.nitro_service as NITROSVC
import nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsip as NS
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey as CERTKEY
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding import sslvserver_sslcertkey_binding as VsrvrCKeyBdg
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver  as LBVSERVER
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding  import *

from test_dut    import * 
from test_config import * 



def	GenerateNames(prefix,num=0) :
	print 'GenerateNames {}: entering function'.format(prefix)
	i = 1
	try :
		print 'GenerateNames {}: entering while'.format(prefix)
		while True :
			yield '{}_{}'.format(prefix,i)
			i += 1
			if ((num > 0) and (i > num)) :
				break

	finally :
		pass


# Files: nitro_service.py
def	Login(nsip,name='nsroot',passwd='nsroot',timeout=10000) :
	ns = NITROSVC.nitro_service(nsip)
	ns.timeout = 10000
	ns.set_credential(name,passwd)
	ns.login()
	return ns




# Return one NSIP,SNIP,VIP in a dictionary keys by ip type string
def	GetIPS(session) :
	ips = NS.nsip.get(session)
	d = {x.type:x.ipaddress for x in ips}
	return d




def	AddDelOneServerCert(session,certName,certFileName,keyFileName=None,isdel=0):
	ad = ['Add', 'Del']	
	ret = 0
	ckey = CERTKEY.sslcertkey()
	ckey.certkey = certName
	ckey.cert = certFileName
	ckey.key = keyFileName
	try :
		if (isdel == 0) :
			CERTKEY.sslcertkey.add(session,ckey)
		else :
			CERTKEY.sslcertkey.delete(session,ckey)
	except NITROEXCEPTION.nitro_exception as e :
		print 'Failed to %s certkey %s\n' %(ad[isdel],certName) 
		print e.message
		ret = e.errorcode

	return ret




def	AddDelTestServerCerts(session,isdel=0) :
	ret = 0
	for cert in TestServerCerts.keys() :
		key = TestServerCerts[cert]
		namel = cert.partition('.')[0].rpartition('_')

		if namel[0] :
			name = namel[0]
		else :
			name = namel[-1]

		ret = AddDelOneServerCert(session,name,cert,key,isdel)
		if(ret != 0) :
			return ret

	return ret




def	AddDelTestServerCertsTuples(session,isdel=0) :
	ret = 0
	for name in TestServerCertsTuple.keys() :
		cert = TestServerCertsTuple[name][0]
		key  = TestServerCertsTuple[name][1]

		ret = AddDelOneServerCert(session,name,cert,key,isdel)
		if(ret != 0) :
			return ret

	return ret





def	LinkUnlinkCertList(session,linklist,isunlink=0) :
	ret = 0
	links = [CERTKEY.sslcertkey() for i in range(len(linklist))]

	try :
		for i in range(len(linklist)) :
			links[i].certkey = linklist[i][0]
			links[i].linkcertkeyname = linklist[i][1]

			if(isunlink == 0) :
				CERTKEY.sslcertkey.link(session,links[i])
			else :
				CERTKEY.sslcertkey.unlink(session,links[i])

	except NITROEXCEPTION.nitro_exception as e :
		ret = e.errorcode
		print 'Failed to link unlink certkey {0} {1}\n'.format(links[i].certkey,links[i].linkcertkeyname)
		print e.message
	
	return ret




def AddDelSSLVserver(session,vsrvrlist,isdel=0) :
	sslv = LBVSERVER.lbvserver()
	for tup in vsrvrlist :
		sslv.name = tup[0]
		sslv.servicetype = tup[1]
		sslv.port = tup[2]
		sslv.ipv46 = DUT.VIP
	
		if (isdel == 0) :
			LBVSERVER.lbvserver.add(session,sslv)
		else : 
			LBVSERVER.lbvserver.delete(session,sslv)




def AddDelOneSvc(session,svc,type,ip,port,isdel=0) :
	ret = 0
	try :
		s = NSSVC()
		s.name = svc
		s.ip   = ip
		s.port = port
		s.servicetype = type
		
		if(isdel == 0) :
			NSSVC.add(session,s)
		else :
			NSSVC.delete(session,s)

	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode

	return ret





def AddDelSvc(session,isdel=0) :
	ret = 0
	try :
		for (name,type,ip,port) in TestBEServices :
			AddDelOneSvc(session,name,type,ip,port,isdel)

	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode

	return ret



			
def BindUnbindOneVsrvrCKey(session,server,certkey,isunbind=0,issni=False,isca=False,ocspcheck=False,crlcheck=False) :
	ret = 0
	try :
		vckey = VsrvrCKeyBdg()
		vckey.vservername = server 
		vckey.certkeyname = certkey 
		VsrvrCKeyBdg.add(sess,vckey)
	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode

	return ret



def BindUnbindVsrvrCKey(session) :
	ret = 0
	try :
		for (v,c) in TestSSLVserverCertkeyBindings :
			BindUnbindOneVsrvrCKey(session,v,c)
	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode

	return ret



def BindUnbindOneVsrvrSvc(session,server,service,isunbind=0) :
	ret = 0
	try :
		B = lbvserver_service_binding()
		B.name = server
		B.servicename = service
		if(isunbind == 0) :
			B.add(session,B)
		else :
			B.delete(session,B)

	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode

	return ret




def BindUnbindVsrvrSvc(session,isunbind=0) :
	for (v,s) in TestVsrvrSvcBindings :
		ret = BindUnbindOneVsrvrSvc(session,v,s,isunbind)
	return ret


def	GetAllCipherSuites(session) :
	C = SSLCIPHERSUITE.get(sess)
	for c in C :
		yield c







def	SetSSLSvcVersion(session,svc,ssl3=1,tls1=1,tls11=1,tls12=1,isupdate=1) :
	ret = 0
	try :
		s = SSLSVC()
		s.servicename = svc

		if(ssl3 == 1) :
			s.ssl3 = SSLSVC.Ssl3.ENABLED
		else :		
			s.ssl3 = SSLSVC.Ssl3.DISABLED

		if(tls1 == 1) :
			s.tls1 = SSLSVC.Tls1.ENABLED
		else :		
			s.tls1 = SSLSVC.Tls1.DISABLED

		if(tls11 == 1) :
			s.tls11 = SSLSVC.Tls11.ENABLED
		else :		
			s.tls11 = SSLSVC.Tls11.DISABLED

		if(tls12 == 1) :
			s.tls12 = SSLSVC.Tls12.ENABLED
		else :		
			s.tls12 = SSLSVC.Tls12.DISABLED

		if(isupdate == 1) :
			SSLSVC.update(session,s)

	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode

	return ret





def	SetSSLSvcDH(session,svc,dhfile='dh2048',dh=1,dhcount=0,isupdate=1) :
	ret = 0
	try :
		s = SSLSVC()
		s.servicename = svc
		if(dh == 1) :
			s.dh = SSLSVC.Dh.ENABLED
		else :
			s.dh = SSLSVC.Dh.DISABLED
		s.dhcount = dhcount
		s.dhfile = dhfile

		if(isupdate == 1) :
			SSLSVC.update(session,s)

	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode
	return ret





def	SetSSLSvcERsa(session,svc,ersa=1,ersacount=0,isupdate=1) :
	ret = 0
	try :
		s = SSLSVC()
		s.servicename = svc
		if(ersa == 1) :
			s.ersa = SSLSVC.Ersa.ENABLED
		else :
			s.ersadh = SSLSVC.Ersa.DISABLED
		s.ersacount = ersacount

		if(isupdate == 1) :
			SSLSVC.update(session,s)

	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode
	return ret





def	SetSSLSvcMisc(session,svc,snienable=0,serverauth=0,commonname=None,sessreuse=0,sesstimeout=120,isupdate=1) :
	ret = 0
	try :
		if not isinstance(svc,SSLSVC) :
			s = SSLSVC()
			s.servicename = svc
		else :
			s = svc

		if(snienable == 1) :
			s.snienable = SSLSVC.Snienable.ENABLED
		else :
			s.snienable = SSLSVC.Snienable.DISABLED

		if(serverauth == 1) :
			s.serverauth = SSLSVC.Serverauth.ENABLED
		else :
			s.serverauth = SSLSVC.Serverauth.DISABLED

		if(sessreuse == 1) :
			s.sessreuse = SSLSVC.Sessreuse.ENABLED 
			s.sesstimeout = sesstimeout 
		else :
			s.sessreuse = SSLSVC.Sessreuse.DISABLED 

		s.commonname = commonname 

		if(isupdate == 1) :
			SSLSVC.update(session,s)

	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode
	return ret




def Gen_SSLBESvc() :
	sslsvclist = [tup[0] for tup in TestBEServices if tup[1] in ['SSL','SSL_TCP']]
	for name in sslsvclist :
		svc = SSLSVC()
		svc.servicename = name
		print type(svc)
		print type(name)
		yield svc







sess = Login('10.102.28.201')
d = GetIPS(sess)
DUT.NSIP 	= d[NS.nsip.Type.NSIP]
DUT.VIP 	= d[NS.nsip.Type.VIP]
DUT.SNIP 	= d[NS.nsip.Type.SNIP]

#AddDelTestServerCertsTuples(sess,0)
#LinkUnlinkCertList(sess,TestServerCALink,0)
#LinkUnlinkCertList(sess,TestServerLink,0)
#AddDelSSLVserver(sess,TestSSLVservers,0)
#BindUnbindVsrvrCKey(sess)

#AddDelSvc(sess,0)
#svclist = [tup[0] for tup in TestBEServices if tup[1] in ['SSL','SSL_TCP']]
#for name in svclist :
#	SetSSLSvcVersion(sess,name,ssl3=1,tls1=0,tls11=0,tls12=1)
#	SetSSLSvcDH(sess,name,dhfile='dh_2048',dh=1,dhcount=1000)
#	SetSSLSvcERsa(sess,name,ersa=1,ersacount=501)
#	SetSSLSvcMisc(sess,name,snienable=1,serverauth=1,commonname='servername',sessreuse=0)

#G = Gen_SSLBESvc()
#for g in G :
#	SetSSLSvcMisc(sess,g,snienable=0,serverauth=1,commonname='ashoke',sessreuse=0,sesstimeout=120,isupdate=1)

#BindUnbindVsrvrSvc(sess,1)
A = GenerateNames('bubu')
B = GenerateNames('ashoke',10)
C = [1,2]
J = zip(A,B,C)
print J
J = zip(A,B)
print J

