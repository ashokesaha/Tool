from	TestException           import *
from	test_dut		import *
from	test_util		import *
import  io
import  requests

from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslciphersuite import sslciphersuite as SSLCIPHERSUITE
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcipher_sslciphersuite_binding import *
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice import sslservice as SSLSVC
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey as CERTKEY
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice_sslcertkey_binding import *



class	BaseTest(object) :
	#desc             = "This is a test for .."
	#TestList         = []
	#TestSession      = None
	_VsrvrNameSpace   = 'vsrvr_'
	_ServiceNameSpace = 'svc_'
	_NameSpaceId      = 1
	_BENameSpaceId    = 1
	_testId           = 1
	_PortSpace        = 8001 

        def __init__(self) :
		#self.nsip               = nsip
		self.DUT                = None
		self.session            = None
		
		self.logfile            = None
		self.logio              = None
		
		self.cipherFilter       = None
		self.cipherALLList      = set()
		self.cipherList         = set()
		self.cipherDHList       = set()
		self.cipherDDHList      = set()
		self.cipherEXPList      = set()
		self.cipherDESList      = set()
		self.cipherNULLList     = set()
		self.cipherECDHEList    = set()

                self.cipherSSLv3List    = set()
                self.cipherTLS1List     = set()
		self.cipherTLS12List    = set()
		self.cipherFilterList   = set()
		
		self.serviceList        = []
		self.vsrvrList          = []
		self.vsrvrSvcBind       = []
		self.beServers          = []
		self.botList            = []
		self.urlList            = []

		self.vsrvrNameSpace     = self.__class__._VsrvrNameSpace   + '_' + str(self.__class__._NameSpaceId)
		self.serviceNameSpace   = self.__class__._ServiceNameSpace + '_' + str(self.__class__._NameSpaceId)
                self.PortSpace          = self.__class__._PortSpace
                self.beID               = self.__class__._BENameSpaceId
                self.testId             = self.__class__._testId


                self.__class__._testId = self.__class__._testId + 1
                self.__class__._PortSpace = self.__class__._PortSpace + 1000
                self.__class__._NameSpaceId =  self.__class__._NameSpaceId + 1000
                self.__class__._BENameSpaceId =  self.__class__._BENameSpaceId + 1000
		

	def	Setup(self) :
		SetupFn(self)	


	def	Start(self) :
		StartFn(self)

	def     Prompt(self) :
                pass
        


        def OpenLog(self,name=None) :
                if self.logio :
                        self.CloseLog()
        
                if name :
                        self.logfile = name + '-' + self.nsip
                else :
                        name = self.__class__.__name__ + '-' + str(self.testId)
                        self.logfile = name + '.log'
                
                self.logio = io.open(self.logfile, mode='at', buffering=1024)


    

        def Log(self,b) :
                self.logio.write(unicode(b))
                print b

    

        def CloseLog(self) :
                if not self.logio :
                        return
        
                self.logio.flush()
                self.logio.close()
                self.logio = None




        def  WaitServiceUPDown(self,isup=1) :
                done = False
                svcNameList = [s.name for s in self.serviceList]

                if (isup == 1) :
                        state = 'UP'
                else :
                        state = 'DOWN'
                

                while True :
                        svcList = NSSVC.get(self.DUT.SESSION,svcNameList)
                        for s in svcList :
                                if s.svrstate != 'UP' :
                                        break
                                else :
                                        done = True
                
                                if not done :
                                        time.sleep(2)
                                continue

                        return done


	@classmethod
	def About(cls) :
		return cls.desc


	@classmethod
	def	RegisterTest(cls,t) :
		if not isinstance(t,BaseTest) :
			raise TestException(1)
		cls.TestList.append(t)







##################################################################
def	SetupFn(bt) :
	print 'this is SetupFn of BaseTest'
	pass






#################################################################
def	StartFn(bt) :
	bt.TestSession = Login(bt.nsip)
	d = GetIPS(bt.TestSession)






##################################################################
def     AddHTTPVservers(harness,num) :
        for i in range(1,num+1,1) :
                name = harness.vsrvrNameSpace + '-' + str(i)
                sslv = LBVSERVER.lbvserver()
                sslv.name = name
                sslv.servicetype = 'HTTP'
                sslv.port = harness.PortSpace
                harness.PortSpace = harness.PortSpace + 1
                sslv.ipv46 = harness.DUT.VIP

                harness.vsrvrList.append(sslv)

        LBVSERVER.lbvserver.add(harness.DUT.SESSION, harness.vsrvrList)
        return   harness.vsrvrList






##################################################################
def     AddSSLServices(harness) :
        nameList = []
        for beS in harness.beServers :
                 for i in range(6) :
                        s       = NSSVC()
                        s.ip    = beS.ip        
                        s.port  = 4443 + i
                        s.name  = 'sslsvc-' + str(harness.beID) + s.ip + '-' + str(s.port)
                        nameList.append(s.name)
                        s.servicetype = 'SSL'
                        s.maxreq = 1
                        harness.serviceList.append(s)

        NSSVC.add(harness.DUT.SESSION,harness.serviceList)
        harness.SSLServiceList = SSLSVC.get(harness.DUT.SESSION,nameList)

        # Without explicitly cleaning up these fields I cannot update
        # the service.
        
        for s in harness.SSLServiceList :
                s.dhfile = None
                s.cipherurl = None
                s.sslv2url = None
                s.clientcert = None
                s.commonname = None
                s.pushenctrigger = None
                s.dtlsprofilename = None
                s.sslprofile = None
                s.ersa = 'DISABLED'
                s.ersacount=0
                
        SSLSVC.update(harness.DUT.SESSION, harness.SSLServiceList)






##################################################################
def     BindServerService(harness) :
        for (x,y) in zip(harness.vsrvrList,harness.serviceList) :
                B = lbvserver_service_binding()
                B.name = x.name
		B.servicename = y.name
                harness.vsrvrSvcBind.append(B)

        lbvserver_service_binding.add(DUT.SESSION,harness.vsrvrSvcBind)


                




##################################################################
def     FillCiphers(harness) :
        l = [str(c.ciphername) for c in SSLCIPHERSUITE.get(harness.DUT.SESSION)]
        s1 = set(l)
        
        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "DH")]
        s2 = set(l)
        
        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "EXP")]
        s3 = set(l)
        
        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "DES")]
        s4 = set(l)
        
        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "NULL")]
        s5 = set(l)
        
        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "ECDHE")]
        s6 = set(l)

        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "AES-GCM")]
        s7 = set(l)

        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "SHA2")]
        s8 = set(l)

        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "DSS")]
        s9 = set(l)

        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "EXPORT40")]
        s10 = set(l)

        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "SSLv2")]
        s11 = set(l)

        l = [str(d.ciphername) for d in sslcipher_sslciphersuite_binding.get(harness.DUT.SESSION, "ADH")]
        s12 = set(l)
       
       

        harness.cipherDHList       = s2 - s11
        harness.cipherADHList      = s12
	harness.cipherEXPList      = s3.union(s10) - s11
	harness.cipherDESList      = s4 - s11
	harness.cipherNULLList     = s5 - s11
	harness.cipherECDHEList    = s6 - s11
	harness.cipherGCMList      = s7 - s11
	harness.cipherSHA2List     = s8 - s11
	harness.cipherDSSList      = s9 - s11
	harness.cipherList         = s1 - s3.union(s10).union(s5).union(s11)
	harness.cipherALLList      = s1
	if harness.cipherFilter :
                harness.cipherFilterList = {c for c in s1 if (c.find(harness.cipherFilter) != -1)}
	
	



# The dictionary elements are like this :-
# {certname : (certfilename, keyflename), ... }
##################################################################
def     AddDelCertkey(session, certDict, isdel=0) :
        ret = True
        certlist = []

        for certname in certDict.keys() :
                t = certDict[certname]
                certfilename = t[0]
                keyfilename  = t[1]

                ckey = CERTKEY.sslcertkey()
                ckey.certkey = certname
                ckey.cert = certfilename
                ckey.key = keyfilename
                certlist.append(ckey)
                
        try :
                if (isdel == 0) :
                        CERTKEY.sslcertkey.add(session,certlist)
		else :
                        CERTKEY.sslcertkey.delete(session,certlist)

        except NITROEXCEPTION.nitro_exception as e :
		print 'Failed to %s certkey %s\n' %(ad[isdel],certName) 
		print e.message
		ret = False

	return ret






# The linklist is list of tuples of the form (certkey,linkcertkey)
##################################################################
def	LinkUnlinkCertList(session,linklist,isunlink=0) :
        ret = True
        links = []
        for (x,y) in linklist :
                link = CERTKEY.sslcertkey()
                link.certkey = x
                link.linkcertkeyname = y
                links.append(link)

        try :
                if(isunlink == 0) :
                        CERTKEY.sslcertkey.link(session,links)
                else :
                        CERTKEY.sslcertkey.unlink(session,links)

        except NITROEXCEPTION.nitro_exception as e :
                print 'Failed to linkinlink'
		ret = False
		print e.message
	
	return ret

        


##########################################################################
def     BindUnbindServiceCert(session,serviceList,certList,isunbind = 0) :
        ret = True
        bindings = []
        for (x,y) in zip(serviceList,certList) :
                b = sslservice_sslcertkey_binding()
                b.servicename = x
                b.certkeyname = y
                bindings.append(b)

        try :
                if(isunbind == 0) :
                        sslservice_sslcertkey_binding.add(session,bindings)
                else :
                        sslservice_sslcertkey_binding.delete(session,bindings)
                
        except NITROEXCEPTION.nitro_exception as e :
                print 'Failed to linkinlink'
		ret = False
		print e.message
	
	return ret





########################################################################
def     BindUnbindAllServiceCert(session,harness,isunbind = 0) :
        ret = True
        bindings = []

        for(x,y) in zip(harness.serviceList,harness.clientCertDict.keys()) :
                b = sslservice_sslcertkey_binding()
                b.servicename = x.name
                b.certkeyname = y
                bindings.append(b)        

        l = [(b.servicename,b.certkeyname) for b in bindings]
        
        try :
                if(isunbind == 0) :
                        sslservice_sslcertkey_binding.add(session,bindings)
                else :
                        sslservice_sslcertkey_binding.delete(session,bindings)

        except NITROEXCEPTION.nitro_exception as e :
                print 'Failed to BindUnbind cert to service'
		ret = False
		print e.message
	
	return ret

