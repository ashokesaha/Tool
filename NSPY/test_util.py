import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver
import nssrc.com.citrix.netscaler.nitro.service.nitro_service as NITROSVC
import nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsip as NS
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey as CERTKEY
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding import sslvserver_sslcertkey_binding as VsrvrCKeyBdg
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver  as LBVSERVER
from test_dut    import * 
from test_config import * 


		

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



def BindUnbindVserverServerCertkey(session,server,certkey,isunbind=0,issni=False,isca=False,ocspcheck=False,crlcheck=False) :
	ret = 0
	try :
		vckey = VsrvrCKeyBdg()
		vckey.vservername = 'vsOne'
		vckey.certkeyname = 'server2048'
		VsrvrCKeyBdg.add(sess,vckey)
	except NITROEXCEPTION.nitro_exception as e :
		print 'Nitro exception:::: {0}'.format(e.message)
		ret = e.errorcode

	return ret





sess = Login('10.102.28.201')
d = GetIPS(sess)
DUT.NSIP = d[NS.nsip.Type.NSIP]
DUT.VIP = d[NS.nsip.Type.VIP]
DUT.SNIP = d[NS.nsip.Type.SNIP]
print DUT.NSIP
print DUT.VIP
print DUT.SNIP

AddDelTestServerCertsTuples(sess,0)
LinkUnlinkCertList(sess,TestServerCALink,0)
LinkUnlinkCertList(sess,TestServerLink,0)
AddDelSSLVserver(sess,TestSSLVservers,0)

try :
	vckey = VsrvrCKeyBdg()
	vckey.vservername = 'vsOne'
	vckey.certkeyname = 'server2048'
	VsrvrCKeyBdg.add(sess,vckey)
except NITROEXCEPTION.nitro_exception as e :
	print 'Nitro exception:::: {0}'.format(e.message)


