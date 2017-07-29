import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl as SSL
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbmonitor as LBMON
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbmonitor_service_binding as LBMONSVCBINDING
from   nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice_sslciphersuite_binding import *
from   nssrc.com.citrix.netscaler.nitro.resource.config.basic.service import service as NSSVC
from   nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice import sslservice as SSLSVC

from	test_util	import *
from	TestException	import *

import time

def Gen_SSLBESvcX(prefix='ssl_svc', count=1, port=443, type='SSL') :

	if not DUT.SESSION :
		raise TestException(100)
	if not DUT.SNIP :
		raise TestException(101)

	nameG = GenerateNames(prefix,count)
	numG  = GenerateNumbers(port,count)

        serviceList = []
        
	for name in nameG :
		port = numG.next()
		ip   = BESERVER
		sess = DUT.SESSION

		svc = AddDelOneSvc(sess,name,type,ip,port,isdel=0)
		#yield svc
		serviceList.append(svc)
	return serviceList


def Gen_SSLBESvc(prefix='ssl_svc', count=1, port=443, type='SSL') :

	if not DUT.SESSION :
		raise TestException(100)
	if not DUT.SNIP :
		raise TestException(101)

	nameG = GenerateNames(prefix,count)
	numG  = GenerateNumbers(port,count)
        
        serviceList = []
        
	for name in nameG :
		port = numG.next()
		ip   = BESERVER
		
		s = NSSVC()
		s.name = name
		s.ip   = ip
		s.port = port
		s.servicetype = type
		s.maxreq = 1

		serviceList.append(s)

	
        NSSVC.add(DUT.SESSION,serviceList)
	return serviceList





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


def  WaitServiceUP(session,nameList) :
        done = False
        while True :
                svcList = NSSVC.get(session,nameList)
                for s in svcList :
                        if s.svrstate != 'UP' :
                                break
                else :
                        done = True
                
                if not done :
                        time.sleep(3)
                        continue

                return done




def AddDelSvc(session,isdel=0) :
	ret = 0
	try :
		for (name,type,ip,port) in TestBEServices :
			AddDelOneSvc(session,name,type,ip,port,isdel)

	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode

	return ret




def  IsSvcUP(session,svc) :
        s = SSLSVC.get(session,svc)
        if not s :
                raise TestException(101)
        



def	SetSSLSvcVersion(sess,svcList,ssl3=1,tls1=1,tls11=1,tls12=1) :
	ret = 0

	try :

                for s in svcList :
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

                SSLSVC.update(sess,svcList)
                        
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

 

def     GetCipherBinding(sess,svcname) :
        ret = 0
        b = sslservice_sslciphersuite_binding.get(sess,svcname)
        return b



def     DelAllCipherBinding(sess,svcname) :
        B = GetCipherBinding(sess,svcname)

        for b in B :
                if not b.ciphername :
                        continue
                
                try :
                        print 'DelAllCipherBinding : {} {}'.format(b.ciphername,b.servicename)
                        sslservice_sslciphersuite_binding.delete(sess,b)
                except NITROEXCEPTION.nitro_exception as e :
                        print 'exception: {} {}'.format(b.ciphername,b.servicename)



def     BindCiphersuite(sess,svcname,ciphername) :
        bndg = SSL.sslservice_sslciphersuite_binding.sslservice_sslciphersuite_binding()
        bndg.ciphername = ciphername
        bndg.servicename = svcname
        sslservice_sslciphersuite_binding.add(sess,bndg)
        return bndg



def     PrepareBatchCipherBinding(svcList,ciphername) :
        bindinglist = []
        for svc in svcList :
                bndg = SSL.sslservice_sslciphersuite_binding.sslservice_sslciphersuite_binding()
                bndg.ciphername = ciphername
                bndg.servicename = svc.name
                bindinglist.append(bndg)
        return bindinglist



def     UpdateBatchCipherBinding(bindinglist, newciphername) :
        for b in bindinglist :
                b.ciphername = newciphername



def     BindUnbindBatchCipherBinding(sess,bindinglist,isunbind=False) :
        ret = True
        
        try :
                if not isunbind :
                        sslservice_sslciphersuite_binding.add(sess, bindinglist)
                else :
                        sslservice_sslciphersuite_binding.delete(sess,bindinglist)

        except NITROEXCEPTION.nitro_exception as e :
                ret = False            

        return ret                



def     AddTCPMonitor(sess,name,interval=5,downtime=5) :
        monitor = LBMON.lbmonitor()
        monitor.monitorname = name
        monitor.type = LBMON.lbmonitor.Type.TCP
        monitor.downtime = downtime
        monitor.interval = interval
        LBMON.lbmonitor.add(sess,monitor)
        return monitor


def     BindMonitor(sess,svcname,monitorname) :
        binding = LBMONSVCBINDING.lbmonitor_service_binding()
        binding.servicename = svcname
        binding.monitorname = monitorname
        LBMONSVCBINDING.lbmonitor_service_binding.add(sess,binding)


        
def     BindMonitorServiceList(sess,serviceList,monitorname) :
        l = []

        for svc in serviceList :
                binding = LBMONSVCBINDING.lbmonitor_service_binding()
                binding.servicename = svc.name
                binding.monitorname = monitorname
                l.append(binding)
        
        LBMONSVCBINDING.lbmonitor_service_binding.add(sess,l)
        return l

        
     



        

