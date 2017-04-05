
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
			('vsOne',	'SSL',	4443),
			('vsTwo',	'SSL',	4445),
			('vsThree',	'SSL',	4447),
			('vsFour',	'SSL',	4449),
			('vsFive',	'SSL',	4451),
			('vsSix',	'SSL',	4453),
			('vsSeven',	'SSL',	4455),
			('vsEight',	'SSL',	4457),
			('vsNine',	'SSL',	4459),
			('vsTen',	'SSL',	4461) ]
