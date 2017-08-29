import os
import paramiko

#client = paramiko.client.SSHClient()
#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect('10.102.28.235',username='nsroot', password='nsroot')
#sftp = client.open_sftp()
#ldir = sftp.listdir()
#l = [str(x) for x in ldir]
#sftp.put('C:\\Users\\ashokes\\Miniconda2\\NSPY\\TestCerts.tgz','/nsconfig/ssl/TestCerts.tgz')

os.chdir('C:\\Users\\ashokes\\Miniconda2\\NSPY\\Certs')
files = os.listdir('C:\\Users\\ashokes\\Miniconda2\\NSPY\\Certs')
c = [certs for certs in files if certs.find('_cert') >= 0]
k = [keys for keys in files if keys.find('_key') >= 0]



cert_type = ['client', 'Server']
cert_sizes = [1024,2048,4096]
md_types = ['sha1','sha256','sha384']
cert_list = []


for ct in cert_type :
    for cs in cert_sizes :
        for mt in md_types :
            prefix = ct + str(cs) + '_' + mt
            cert = prefix + '_cert.pem'
            key  = prefix + '_key.pem'
            cert_list.append((prefix,cert,key))

print cert_list



#client = paramiko.client.SSHClient()
#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect('10.102.28.235',username='nsroot', password='nsroot')
#sftp = client.open_sftp()

#for f in files :
#    d = '/nsconfig/ssl/' + f
#    print '{} {}'.format(f,d)
#    sftp.put(f,d)


#cert_sizes = [1024,2048]
#md_types = ['sha1','sha256','sha384']


    

