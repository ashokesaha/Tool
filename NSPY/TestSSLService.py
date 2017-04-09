import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION
from nssrc.com.citrix.netscaler.nitro.resource.config.basic.service import service as NSSVC
from   nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice import sslservice as SSLSVC

from	test_util	import *
from	TestException	import *


def Gen_SSLBESvc(prefix='ssl_svc', count=1, port=443, type='SSL') :

	if not DUT.SESSION :
		raise TestException(100)
	if not DUT.SNIP :
		raise TestException(101)

	nameG = GenerateNames(prefix,count)
	numG  = GenerateNumbers(port,count)

	for name in nameG :
		port = numG.next()
		ip   = DUT.SNIP
		sess = DUT.SESSION

		svc = AddDelOneSvc(sess,name,type,ip,port,isdel=0)
		yield svc



def AddDelOneSvc(session,svc,type,ip,port,isdel=0) :
	s = None 
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
		s = None
		ret = e.errorcode

	return s 





def AddDelSvc(session,isdel=0) :
	ret = 0
	try :
		for (name,type,ip,port) in TestBEServices :
			AddDelOneSvc(session,name,type,ip,port,isdel)

	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode

	return ret




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

