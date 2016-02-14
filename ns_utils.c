public int	AddSSLCertKey(NSObject nsO)
{
	int			ret = 0;
	sslcertkey	sslcertkey_obj;

	try
	{
		sslcertkey_obj = new sslcertkey();
		sslcertkey_obj.set_certkey(nsO.certKeyName);
		sslcertkey_obj.set_cert(nsO.certFileName);
		sslcertkey_obj.set_key(nsO.keyFileName);
		sslcertkey.add(ns_session,sslcertkey_obj);

	} catch(Exception e) {
		System.out.println("Java Error -> " +e.getMessage());
		ret = -1;
	}

	return ret;
}



public int	BindSSLVserverCertkey(NSObject nsO)
{
	int								ret = 0;
	sslvserver_sslcertkey_binding	sslvserver_sslcertkey_binding_obj;

	try
	{
		sslvserver_sslcertkey_binding_obj = new sslvserver_sslcertkey_binding();
		sslvserver_sslcertkey_binding_obj.set_vservername(nsO.vserverName);
		sslvserver_sslcertkey_binding_obj.set_certkeyname(nsO.certKeyName);
		sslvserver_sslcertkey_binding.add(ns_session,sslvserver_sslcertkey_binding_obj);

	} catch(Exception e) {
		System.out.println("Java Error -> " +e.getMessage());
		ret = -1;
	}

	return ret;
}



public int	AddHTTPService(NSObject nsO)
{
	return AddService(nsO.serviceName,nsO.serverName,nsO.port,"HTTP");
}
public int	AddSSLService(NSObject nsO)
{
	return AddService(nsO.serviceName,nsO.serverName,nsO.port,"SSL");
}

private int	AddService(String name,String server,int port,String type)
{
	int		ret = 0;
	service	service_obj;

	try
	{
		service_obj.set_name(name);
		service_obj.set_servername(server);
		service_obj.set_port(port);
		service_obj.set_type(type);
		service_obj.add(ns_session,server_obj);
	
	} catch(Exception e) {
		System.out.println("Java Error -> " +e.getMessage());
		ret = -1;
	}

	return ret;
}




public int	BindSSLVserverCipher(NSObject nsO)
{
	int								ret = 0;
	sslvserver_sslcipher_binding	sslvserver_sslcipher_binding_obj;

	try
	{
		sslvserver_sslcipher_binding_obj = new sslvserver_sslcipher_binding();
		sslvserver_sslcipher_binding_obj.set_vservername(nsO.vserverName);
		sslvserver_sslcipher_binding_obj.set_ciphername(nsO.cipherName);
		sslvserver_sslcipher_binding.add(ns_session,sslvserver_sslcipher_binding_obj);

	} catch(Exception e) {
		System.out.println("Java Error -> " +e.getMessage());
		ret = -1;
	}

	return ret;
}


public int	BindSSLServiceCipher(NSObject nsO)
{
	return BindUnbindSSLServiceCipher(ns0,true);
}

public int	UnbindSSLServiceCipher(NSObject nsO)
{
	return BindUnbindSSLServiceCipher(ns0,false);
}


private int	BindUnbindSSLServiceCipher(NSObject nsO, boolean bind)
{
	int								ret = 0;
	sslservice_sslcipher_binding	sslservice_sslcipher_binding_obj;

	try
	{
		sslservice_sslcipher_binding_obj = new sslservice_sslcipher_binding();
		sslservice_sslcipher_binding_obj.set_servicename(nsO.serviceName);
		sslservice_sslcipher_binding_obj.set_ciphername(nsO.cipherName);
		if(bind == true)
			sslservice_sslcipher_binding.add(ns_session,sslservice_sslcipher_binding_obj);
		else
			sslservice_sslcipher_binding.delete(ns_session,sslservice_sslcipher_binding_obj);

	} catch(Exception e) {
		System.out.println("Java Error -> " +e.getMessage());
		ret = -1;
	}

	return ret;
}


public int	BindLBVserverService(NSObject nsO)
{
	int							ret = 0;
	lbvserver_service_binding	lbvserver_service_binding_obj;

	try
	{
		lbvserver_service_binding_obj = new lbvserver_service_binding();
		lbvserver_service_binding_obj.set_name(nsO.vserverName);
		lbvserver_service_binding_obj.set_servicename(nsO.serviceName);
		lbvserver_service_binding.add(ns_session,lbvserver_service_binding_obj);

	} catch(Exception e) {
		System.out.println("Java Error -> " +e.getMessage());
		ret = -1;
	}

	return ret;
}




