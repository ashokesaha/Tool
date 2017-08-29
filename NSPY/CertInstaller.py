import sys
import os
import paramiko
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')
import test_util
import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey as CERTKEY


class  CertInstall :

    def __init__(self) :
        self.certdir = None
        self.allCerts = []
        self.entityCerts = []
        self.caCerts = []



    def SetCertDir(self,dir) :
        ret = True
        try :
            self.certdir  = dir
            os.chdir(dir)
        except WindowError as e :
            self.certdir = None
            ret = False

        return ret



    def  ListEntityCerts(self) :
        files = os.listdir('.')
        cert_type = ['client', 'Server']
        #cert_sizes = [1024,2048,4096]
        cert_sizes = [1024,2048]
        md_types = ['sha1','sha256','sha384']
        cert_list = []

        for ct in cert_type :
            for cs in cert_sizes :
                for mt in md_types :
                    prefix = ct + str(cs) + '_' + mt
                    cert = prefix + '_cert.pem'
                    key  = prefix + '_key.pem'
                    cert_list.append((prefix,cert,key))

        self.entityCerts = cert_list
        return cert_list


    def ListCACerts(self) :
        files = os.listdir('.')
        files = set(files)

        cert_type = ['client', 'Server']
        cert_sizes = [1024,2048,4096]
        #cert_sizes = [1024,2048]

        md_types = ['sha1','sha256','sha384']
        cert_list = []


        l = []
        for ct in cert_type :
            for cs in cert_sizes :
                for mt in md_types :
                    prefix = ct + str(cs) + '_' + mt
                    cert = prefix + '_cert.pem'
                    key  = prefix + '_key.pem'
                    l.append(cert)
                    l.append(key)

        l = set(l)

        files = files - l
        self.caCerts = list(files)
        self.caCerts = [(s.split('_')[0].split('.')[0],s) for s in self.caCerts]
        return self.caCerts



    def  PushToNS(self,nsip) :
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(nsip,username='nsroot', password='nsroot')
        sftp = client.open_sftp()

        files = os.listdir('.')
        for f in files :
            d = '/nsconfig/ssl/' + f
            sftp.put(f,d)



    def	AddDelEntityCerts(self,session,isdel=0) :
        ret = True
        L = []
        for ec in self.entityCerts :
            ckey = CERTKEY.sslcertkey()
            ckey.certkey = ec[0]
            ckey.cert = ec[1]
            ckey.key = ec[2]
            L.append(ckey)

            
        try :
            if (isdel == 0) :
                CERTKEY.sslcertkey.add(session,L)
            else :
                CERTKEY.sslcertkey.delete(session,L)
        except NITROEXCEPTION.nitro_exception as e :
            print e.message
            ret = e.errorcode

        return ret




    def	AddDelCACerts(self,session,isdel=0) :
        ret = True
        L = []
        for ec in self.caCerts :
            ckey = CERTKEY.sslcertkey()
            ckey.certkey = ec[0]
            ckey.cert = ec[1]
            L.append(ckey)
            
        try :
            if (isdel == 0) :
                CERTKEY.sslcertkey.add(session,L)
            else :
                CERTKEY.sslcertkey.delete(session,L)
        except NITROEXCEPTION.nitro_exception as e :
            print 'Exception happened {}'.format(e.message)
            ret = e.errorcode

        return ret



    def  LinkUnlinkCACerts(self,session,isunlink=0) :
        tups = [('OneCA2048','RootServer2048CACert'),
                ('TwoCA1024','OneCA2048'),
                ('ThreeCA2048','TwoCA1024') ]

        links = []
        for (x,y) in tups :
            l = CERTKEY.sslcertkey()
            l.certkey = x
            l.linkcertkeyname = y
            
            links.append(l)

        try :
            if (isunlink == 0) :
                CERTKEY.sslcertkey.link(session,links)
            else :
                CERTKEY.sslcertkey.unlink(session,links)

        except NITROEXCEPTION.nitro_exception as e :
                ret = e.errorcode
                print 'Exception happened {}'.format(e.message)



    def  LinkUnlinkEntityCerts(self,session,isunlink=0) :
        tups = [('Server1024_sha1',     'ThreeCA2048'),
                ('Server1024_sha256',   'ThreeCA2048'),
                ('Server1024_sha384',   'ThreeCA2048'),
                ('Server2048_sha1',     'ThreeCA2048'),
                ('Server2048_sha256',   'ThreeCA2048'),
                ('Server2048_sha384',   'ThreeCA2048')]
                #('Server4096_sha1',     'ThreeCA2048'),
                #('Server4096_sha256',   'ThreeCA2048'),
                #('Server4096_sha384',   'ThreeCA2048')]


        links = []
        for (x,y) in tups :
            l = CERTKEY.sslcertkey()
            l.certkey = x
            l.linkcertkeyname = y
            
            links.append(l)

        try :
            if (isunlink == 0) :
                CERTKEY.sslcertkey.link(session,links)
            else :
                CERTKEY.sslcertkey.unlink(session,links)

        except NITROEXCEPTION.nitro_exception as e :
                ret = e.errorcode
                print 'Exception happened {}'.format(e.message)


    
    def Link(self,sess) :
        print 'CertInstall Link . log in {}'.format(sess.isLogin())
        self.ListEntityCerts()
        self.ListCACerts()
        print 'CertInstall Link : AddDelEntityCerts'
        self.AddDelEntityCerts(sess,isdel=0)
        print 'CertInstall Link : AddDelCACerts'
        self.AddDelCACerts(sess,isdel=0)
        print 'CertInstall Link : LinkUnlinkCACerts'
        self.LinkUnlinkCACerts(sess,isunlink=0)
        print 'CertInstall Link : LinkUnlinkEntityCerts'
        self.LinkUnlinkEntityCerts(sess,isunlink=0)


    def UnLink(self,sess) :
        ci.LinkUnlinkCACerts(sess,isunlink=1)
        ci.LinkUnlinkEntityCerts(sess,isunlink=1)
        ci.AddDelEntityCerts(sess,isdel=1)
        ci.AddDelCACerts(sess,isdel=1)




if __name__ == "__main__":
    ci = CertInstall()
    ci.SetCertDir('C:\\Users\\ashokes\\Miniconda2\\NSPY\\Certs')
    l1 = ci.ListEntityCerts()
    l2 = ci.ListCACerts()
    xmode = 2

    sess = test_util.Login('10.102.28.201')
    
    if xmode == 0 :
        print 'Pushiong cert files to NS'
        ci.PushToNS('10.102.28.201')

    sess = test_util.Login('10.102.28.201')
    #print 'sess login {}'.format(sess.isLogin())
    #sess.logout()
    #print 'sess login {}'.format(sess.isLogin())
    #sess = test_util.Login('10.102.28.201')
  
    if sess :
        if xmode == 0 :
            print 'adding entity certs'
            ci.AddDelEntityCerts(sess,isdel=0)
            print 'adding CA certs'
            ci.AddDelCACerts(sess,isdel=0)
            print 'linking CA certs'
            ci.LinkUnlinkCACerts(sess,isunlink=0)
            print 'linking entity certs'
            ci.LinkUnlinkEntityCerts(sess,isunlink=0)

        if xmode == 1 :
            print 'unlinking CA certs'
            ci.LinkUnlinkCACerts(sess,isunlink=1)
            print 'unlinking entity certs'
            ci.LinkUnlinkEntityCerts(sess,isunlink=1)
            print 'deleting entity certs'
            ci.AddDelEntityCerts(sess,isdel=1)
            print 'deleting CA certs'
            ci.AddDelCACerts(sess,isdel=1)

        if xmode == 2 :
            sess.clear_config(level='basic')
        



    
    
        
