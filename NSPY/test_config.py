
TestServerCerts = {	
		'server2048_cert.pem':'server2048_key.pem',	
		'server4096_cert.pem':'server4096_key.pem',
		'FourCA4096_cert.pem':None,
		'ThreeCA2048_cert.pem':None,
		'TwoCA1024_cert.pem':None,
		'OneCA4096_cert.pem':None,
		'RootServer2048CACert.pem':None }


TestServerCertsTuple = {	
		'server2048'  :('server2048_cert.pem','server2048_key.pem'),
		'server4096'  :('server4096_cert.pem','server4096_key.pem'),
		'FourCA4096'  :('FourCA4096_cert.pem', None),
		'ThreeCA2048' :('ThreeCA2048_cert.pem',None),
		'TwoCA1024'   :('TwoCA1024_cert.pem',  None),
		'OneCA4096'   :('OneCA4096_cert.pem',  None),
		'RootServer2048CACert':('RootServer2048CACert.pem',None) }



TestServerCALink = [	('FourCA4096','ThreeCA2048'),
						('ThreeCA2048','TwoCA1024'),
						('TwoCA1024','OneCA4096'),
						('OneCA4096','RootServer2048CACert')]


TestServerLink = [	('server2048','FourCA4096'),
					('server4096','FourCA4096') ]



TestSSLVservers = [	
			('vsOne',	'SSL',		4443),
			('vsTwo',	'SSL',		4445),
			('vsThree',	'SSL',		4447),
			('vsFour',	'SSL',		4449),
			('vsFive',	'SSL',		4451),
			('vsSix',	'SSL_TCP',	4453),
			('vsSeven',	'SSL_TCP',	4455),
			('vsEight',	'SSL_TCP',	4457),
			('vsNine',	'SSL_TCP',	4459),
			('vsTen',	'SSL_TCP',	4461) ]


TestSSLVserverCertkeyBindings =	[
									('vsOne',	'server2048'),
									('vsTwo',	'server4096'),
									('vsThree',	'server2048'),
									('vsFour',	'server4096'),
									('vsFive',	'server2048'),
									('vsSix',	'server4096'),
									('vsSeven',	'server2048'),
									('vsEight',	'server4096'),
									('vsNine',	'server2048'),
									('vsTen',	'server4096') ]



TestBEServices = [
					('svcOne',	'SSL',		'10.102.28.71',443),
					('svcTwo',	'SSL',		'10.102.28.71',445),
					('svcThree','SSL',		'10.102.28.71',447),
					('svcFour',	'SSL_TCP',	'10.102.28.71',449),
					('svcFive',	'SSL_TCP',	'10.102.28.71',451),
					('svcSix',	'SSL_TCP',	'10.102.28.71',453),
					('svcSeven','HTTP',		'10.102.28.71',80),
					('svcEight','HTTP',		'10.102.28.71',8080),
					('svcNine',	'TCP',		'10.102.28.71',7001),
					('svcTen',	'TCP',		'10.102.28.71',7002) ]



TestVsrvrSvcBindings = [
					('vsOne',	'svcOne'),
					('vsTwo',	'svcTwo'),
					('vsThree',	'svcThree'),
					('vsFour',	'svcFour'),
					('vsFive',	'svcFive'),
					('vsSix',	'svcSix'),
					('vsSeven',	'svcSeven'),
					('vsEight',	'svcEight'),
					('vsNine',	'svcNine'),
					('vsTen',	'svcTen') ]




SSLCipherSuites = []
