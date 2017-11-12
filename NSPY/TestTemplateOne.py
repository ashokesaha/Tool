import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')

import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as                                        NITROEXCEPTION
import nssrc.com.citrix.netscaler.nitro.resource.config.basic.service as                                    NSSVC
import nssrc.com.citrix.netscaler.nitro.resource.config.basic.server as                                     SERVER
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver  as                                    LBVSERVER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver  as                                  SSLVSERVER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey as                                   CERTKEY
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcipher as                                    SSLCIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice as                                   SSLSVC
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslciphersuite as                               SSLCIPHERSUITE
import nssrc.com.citrix.netscaler.nitro.service.nitro_service as                                            NITROSVC
import nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsip as                                          NS
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding  as                    LBVSRVRSVCBINDING
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding as                SSLVSRVRCERTKEYBINDING
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice_sslcertkey_binding as                SSLSVCCERTKEYBINDING


from    test_util       import * 
from    test_dut        import * 
from    test_config     import *
from    TestException   import *
from    CertInstaller   import *
import  requests


class TestTemplateOne(object) :
    def __init__(self,templateName,session,container) :
        self.templateName = templateName
        self.sslvserverlist = None
        self.sslservicelist = None
        self.session = session
        self.container = container


    def PrepareSSLVservers(self,fromport=443) :
        dut = self.container.GetCurDUT()
        vsrvrnamelist = []
        ci = CertInstall()
        certlist = ci.ListServerCerts()
        
        for c in certlist :
            vname = self.templateName + '-vsrvr-' + c[0]
            print 'vserver name {}'.format(vname)
            tup = (vname,'SSL',fromport,dut.vip)
            vsrvrnamelist.append(tup)
            tup = None
            fromport += 1

        return vsrvrnamelist


    def InstallSSLVservers(self,vserverlist) :
        AddDelVserver(self.session,vserverlist,isdel=0)
        self.sslvserverlist = SSLVSERVER.sslvserver.get(self.session)



    def InstallSSLServices(self,num) :
        serverlist = self.GetServers()
        slist = [o.ipaddress for o in serverlist]
        newserverlist = []
        print 'InstallSSLServices: slist {}'.format(slist)
        
        count = 0
        svclist = []
        for bes in self.container.SSLBEServerList :
            if num == 0 :
                break
            s = NSSVC.service()
            sname  = self.templateName + '-svc-' + bes.name
            s.name = sname
            s.ip   = bes.ip
            s.port = bes.listen_port
            s.servicetype = bes.type
            s.maxreq = 1
            svclist.append(s)
            num -= 1
            count += 1
            
            if s.ip not in slist :
                newserverlist.append(s.ip)
                slist.append(s.ip)

        serverlist = []
        for n in newserverlist :
            S = SERVER.server()
            S.name = n
            S.ipaddress = n
            serverlist.append(S)
            print 'Adding server {}'.format(n)
        if len(serverlist) > 0 :
            SERVER.server.add(self.session,serverlist)


        if len(svclist) > 0 :
            try :
                NSSVC.service.add(self.session,svclist)
                self.sslservicelist = NSSVC.service.get(self.session)
            except NITROEXCEPTION.nitro_exception as e :
                print 'Service add failed {}'.format(e.message)

        return count




    def BindSSLCertkey(self) :
        ci = CertInstall()
        certlist = ci.ListServerCerts()

        if not self.sslvserverlist or (len(self.sslvserverlist) != len(certlist)) :
            print 'Cannot BindSSLCertkey : Vserver/Certkey mismatch. Need {} number vservers'.format(len(certlist))
            return 0

        bindings = [(self.sslvserverlist[i].vservername,certlist[i][0]) for i in range(len(self.sslvserverlist))]
        blist = []
        for b in bindings :
            B = SSLVSRVRCERTKEYBINDING.sslvserver_sslcertkey_binding()
            B.vservername = b[0]
            B.certkeyname = b[1]
            blist.append(B)
            
        SSLVSRVRCERTKEYBINDING.sslvserver_sslcertkey_binding.add(self.session,blist)



    def BindSSLServiceCertkey(self) :
        ci = CertInstall()
        certlist = ci.ListClientCerts()

        if not self.sslservicelist or (len(self.sslservicelist) != len(certlist)) :
            print 'Cannot BindSSLCertkey : Vserver/Certkey mismatch. Need {} number services'.format(len(certlist))
            return 0

        bindings = [(self.sslvserverlist[i].servicename,certlist[i][0]) for i in range(len(self.sslservicelist))]
        blist = []
        for b in bindings :
            B = SSLSVCCERTKEYBINDING.sslservice_sslcertkey_binding()
            B.servicename = b[0]
            B.certkeyname = b[1]
            blist.append(B)
            
        SSLSVCCERTKEYBINDING.sslservice_sslcertkey_binding.add(self.session,blist)





    def GetServers(self) :
        l = SERVER.server.get(self.session)
        print 'Installed servers {}'.format(len(l))
        for s in l :
            print '{} {}'.format(s.name,s.ipaddress)

        return l


    def Apply(self) :
        try :
            self.session.relogin()
            self.GetServers()
            
            c = self.InstallSSLServices(10)
            self.BindSSLServiceCertkey()
            
##            vlist = self.PrepareSSLVservers()
##            self.InstallSSLVservers(vlist)
##            self.BindSSLCertkey()
            
        except NITROEXCEPTION as e :
            print 'TestTemplateOne Apply failed. {}'.format(e.message)
        



if __name__ == "__main__":
    sess = Login('10.102.28.201')
    tt = TestTemplateOne('tone')
    vlist = tt.PrepareSSLVservers()
    tt.InstallSSLVservers(sess,vlist)
    tt.BindSSLCertkey(sess)

    svclist = []
    s = NSSVC.service()
    s.name = 'one'
    s.ip   = '10.102.28.72'
    s.port = 4443
    s.servicetype = 'SSL'
    s.maxreq = 1
    svclist.append(s)

    s = NSSVC.service()
    s.name = 'two'
    s.ip   = '10.102.28.72'
    s.port = 4445
    s.servicetype = 'SSL'
    s.maxreq = 1
    svclist.append(s)

    NSSVC.service.add(sess,svclist) 
