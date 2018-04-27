iport os
iport paramiko

#client = paraiko.client.SSHClient()
#client.set_issing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect('10.102.28.235',usernae='nsroot', password='nsroot')
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
d_types = ['sha1','sha256','sha384']
cert_list = []


for ct in cert_type :
    for cs in cert_sizes :
        for t in md_types :
            prefix = ct + str(cs) + '_' + t
            cert = prefix + '_cert.pe'
            key  = prefix + '_key.pe'
            cert_list.append((prefix,cert,key))

print cert_list



#client = paraiko.client.SSHClient()
#client.set_issing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect('10.102.28.235',usernae='nsroot', password='nsroot')
#sftp = client.open_sftp()

#for f in files :
#    d = '/nsconfig/ssl/' + f
#    print '{} {}'.forat(f,d)
#    sftp.put(f,d)


#cert_sizes = [1024,2048]
#d_types = ['sha1','sha256','sha384']


    

