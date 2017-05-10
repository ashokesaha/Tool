import time
import paramiko
from test_config import *


class  HttpServerCtrl (object) :

    LinkSets =[ [['server1024_dh1024_cert.pem','server1024_cert.pem'],
                 ['server2048_dh1024_cert.pem','server2048_cert.pem'],
                 ['server4096_dh1024_cert.pem','server4096_cert.pem'] ],
                [['server1024_dh2048_cert.pem','server1024_cert.pem'],
                 ['server2048_dh2048_cert.pem','server2048_cert.pem'],
                 ['server4096_dh2048_cert.pem','server4096_cert.pem'] ],
                [['server1024_dh4096_cert.pem','server1024_cert.pem'],
                 ['server2048_dh4096_cert.pem','server2048_cert.pem'],
                 ['server4096_dh4096_cert.pem','server4096_cert.pem'] ]  ]

    
    ENV = {'LD_LIBRARY_PATH' : '//usr//local//ssl//lib', 'NAME' : 'ashoke'}
    

    def __init__(self, ip) :
        self.ip = ip
        self.client = None
        self.pkey   = None
        self.fin    = None
        self.fout   = None
        self.ferr   = None

    def connect(self) :
        #self.pkey = pkey = paramiko.RSAKey.from_private_key_file('id_rsa')
        #if not self.pkey :
        #   raise TestException(104)
        
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        #self.client.connect(self.ip, username='root', pkey=self.pkey, look_for_keys=False)
        print 'HTTPDUSER {} HTTPDPASSWD {}'.format(HTTPDUSER,HTTPDPASSWD)
        self.client.connect(self.ip, username=HTTPDUSER, password=HTTPDPASSWD)
        self.command('cd /usr/local/apache2/conf')

                
        self.fin.close()
        self.fout.close()
        self.ferr.close()
        self.fin    = None
        self.fout   = None
        self.ferr   = None
        
        
    def command(self,cmdstr) :
        if self.fin :
            self.fin.close()
            self.fin = None

        if self.fout :
            self.fout.close()
            self.fout = None

        if self.ferr :
            self.ferr.close()
            self.ferr = None

        self.fin,self.fout,self.ferr = self.client.exec_command(cmdstr)


    
    def sanitize(self) :
        ret = 0
        self.command('cd /usr/local/apache2/conf; ls')
        rdstr = ferr.read()
        if(len(rdstr) > 0) :
            ret = 1
            print rdstr
            return ret

        L = [str(line.rstrip('\n')) for line in fout]
        S = set(L)



    def StartStop(self, isstop=0) :
        ret = 0
        if(isstop) :
            self.command('export LD_LIBRARY_PATH=/usr/local/ssl/lib; cd /usr/local/apache2/bin; ./apachectl stop 2>/dev/null')
        else :
            #self.command('export LD_LIBRARY_PATH=/usr/local/ssl/lib; cd /usr/local/apache2/bin; ./apachectl start 2>/dev/null')
            self.command('export LD_LIBRARY_PATH=/usr/local/ssl/lib; cd /usr/local/apache2/bin; ./apachectl start 2>/dev/null')

        rdstr = self.ferr.read()
        if(len(rdstr) > 0) :
            ret = 1
            print rdstr
        return ret


    def LinkOneHTTPDFile(self, tup) :
        ret = 0
        cmdstr = 'cd /usr/local/apache2/conf; rm {1} 2> /dev/null; ln -s {0} {1}'.format(tup[0],tup[1])
        self.command(cmdstr)
        rdstr = self.ferr.read()
        if(len(rdstr) > 0) :
            ret = 1
            print rdstr
        return ret
    

    


    def LinkHTTPDCertSet(self) :
        ret = 0
        for links in self.__class__.LinkSets :
            for link in links :
                ret = self.LinkOneHTTPDCert(link)
                if (ret != 0) :
                    break
            if(ret != 0) :
                break
            yield links

    

    def NumProcess(self,name) :
        cmdstr = 'ps -auxwww |grep {0} | grep -v grep |wc -l'.format(name)
        self.command(cmdstr)
        str = self.fout.read()
        return int(str)


    def ClientAuthOnOff (self,on=False) :
        if not on :
            filename = 'httpd.nocauth.conf'
        else :
            filename = 'httpd.cauth.conf'
        
        self.LinkOneHTTPDFile( (filename,'httpd.conf'))

        while (self.NumProcess('httpd') != 0) :
            self.StartStop(isstop=1)
            time.sleep(1)

        while (self.NumProcess('httpd') == 0) :
            self.StartStop(isstop=0)
            time.sleep(1)

        
        
        
            
    
