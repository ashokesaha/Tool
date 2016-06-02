import java.util.Arrays;
import java.util.List;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.*;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import com.citrix.netscaler.nitro.service.nitro_service;
import com.citrix.netscaler.nitro.exception.nitro_exception;
import com.citrix.netscaler.nitro.resource.config.basic.*;
import com.citrix.netscaler.nitro.resource.config.lb.*;
import com.citrix.netscaler.nitro.resource.config.ssl.*;
import com.citrix.netscaler.nitro.resource.config.ns.*;



public class NitroC {

	private nitro_service 		ns_session;
	private	NSObject			nsO;

	private	String				dutIP;
	private	int					dutPort;
	private	int					listenPort;
	private boolean				isListen;
	private boolean				isTerminate;

	private	String				userName;
	private	String				passwd;


	NitroC(String dutIP,int dutPort,int listenPort)
	{
		this.dutIP		= dutIP;
		this.dutPort	= dutPort;
		this.listenPort	= listenPort;
		this.isListen	= false;
		this.isTerminate	= false;
	}

	public boolean Login(String userName,String passwd)
	{
		if(ns_session != null)
		if(ns_session.isLogin() == true)
			return ns_session.isLogin();

		try
		{
			ns_session = new nitro_service(this.dutIP,"HTTP");
			ns_session.login(userName,passwd);

		} catch (nitro_exception e) {
			System.out.println("Login 5: " + e.getMessage());
			;
		} catch (Exception e) {
			System.out.println("Login 6: " + e.getMessage());
			;
		}
	
		if(ns_session.isLogin() == true)
		{
			this.userName	= userName;
			this.passwd		= passwd;
		}
		return ns_session.isLogin();
	}


	public boolean Listen()
	{
		ServerSocket					Ssock;
		Socket							Sock;
		InputStream						inS;
		OutputStream					ouS;
		InputStreamReader				isR;
		BufferedReader					bfR;
		Gson							gson;
		String							jstring;
		boolean							ret;
		String							Rstr;
		byte							B[] = new byte[2];

		if(isListen == true)
			return isListen;

		gson = new GsonBuilder().create();

		isListen	= true;
		
		try  {
			Ssock		= new ServerSocket(this.listenPort);
			Sock		= Ssock.accept();
			inS			= Sock.getInputStream();
			ouS			= Sock.getOutputStream();
			isR			= new InputStreamReader(inS);
			bfR			= new BufferedReader(isR);

		} catch (IOException ioe) {
			isListen = false;
			System.out.println(ioe.getMessage());
			return false;
		}

		while (isTerminate == false)
		{
			try 
			{
				//Sock		= Ssock.accept();
				//inS			= Sock.getInputStream();
				//ouS			= Sock.getOutputStream();
				//isR			= new InputStreamReader(inS);
				//bfR			= new BufferedReader(isR);

				
				nsO			= gson.fromJson(bfR, NSObject.class);
				if(nsO == null)
				{
					System.out.println("Failed to create nsO\n");
					isTerminate = true;
				}

				ret			= Execute(nsO);

				RespObj R 	= new RespObj(ret);
				Rstr 		= gson.toJson(R);
				System.out.println("writing Rstr: " + Rstr);
				OutputStreamWriter	oWr = new OutputStreamWriter(ouS);
				oWr.write(Rstr,0,Rstr.length());
				oWr.flush();

			} catch (IOException ioe) {
				isListen = false;
				System.out.println(ioe.getMessage());
			}
		}

		//Close sockets and streams

		return isListen;
	}



	private boolean	AddDelCertKey(NSObject nsO) 
	{
		if(nsO.isDelete == true)
			return	AddCertKey(nsO);
		else
			return	DelCertKey(nsO);
	}

	private boolean	AddCertKey(NSObject nsO) 
	{
		boolean			ret = true;
		sslcertkey		sslcertkey_obj;

		try
		{
		sslcertkey_obj	= new sslcertkey();
		sslcertkey_obj.set_certkey(nsO.certKeyName);
		sslcertkey_obj.set_cert(nsO.certFileName);
		sslcertkey_obj.set_key(nsO.keyFileName);
		sslcertkey.add(ns_session,sslcertkey_obj);
		
		} catch(Exception e) {
			System.out.println("Java Error -> " +e.getMessage());
			ret = false;
		}
		return ret;
	}

	private boolean	DelCertKey(NSObject nsO) 
	{
		boolean			ret = true;

		try
		{
		sslcertkey.delete(ns_session,nsO.certKeyName);
		
		} catch(Exception e) {
			System.out.println("Java Error -> " +e.getMessage());
			ret = false;
		}
		return ret;
	}


	private boolean	BindUnbindCertKey(NSObject nsO) 
	{
		boolean			ret = true;
		sslvserver_sslcertkey_binding	obj_1;
		sslservice_sslcertkey_binding	obj_2;

		try
		{
			if(nsO.isVserver == true)
			{
				obj_1 = new sslvserver_sslcertkey_binding();
				obj_1.set_certkeyname(nsO.certKeyName);
				obj_1.set_vservername(nsO.vserverName);

				if(nsO.isCACert == true)
					obj_1.set_ca(true);

				if(nsO.isSNICert == true)
					obj_1.set_snicert(true);

				if(nsO.isUnbind)
					sslvserver_sslcertkey_binding.delete(ns_session,obj_1);
				else
					sslvserver_sslcertkey_binding.add(ns_session,obj_1);
			}
			else
			{
				obj_2 = new sslservice_sslcertkey_binding();
				obj_2.set_certkeyname(nsO.certKeyName);
				obj_2.set_servicename(nsO.serviceName);

				if(nsO.isCACert == true)
					obj_2.set_ca(true);

				if(nsO.isSNICert == true)
					obj_2.set_snicert(true);

				if(nsO.isUnbind)
					sslservice_sslcertkey_binding.delete(ns_session,obj_2);
				else
					sslservice_sslcertkey_binding.add(ns_session,obj_2);
			}

		} catch(Exception e) {
			System.out.println("Java Error -> " +e.getMessage());
			ret = false;
		}

		return ret;
	}



	public boolean	AddDelHTTPVserver(NSObject nsO)
	{
		if(nsO.isDelete == false)
			return AddVserver(nsO.vserverName,nsO.ipAddr,nsO.port, "HTTP"); 
		else
			return	DelVserver(nsO.vserverName);
	}
	public boolean	AddDelSSLVserver(NSObject nsO) 
	{
		if(nsO.isDelete == false)
			return AddVserver(nsO.vserverName,nsO.ipAddr,nsO.port, "SSL"); 
		return false;
	}

	public boolean	AddVserver(String name, String ip, int port,String type) 
	{
		boolean					ret = true;
		lbvserver				lbvserver_obj;

		try
		{
		lbvserver_obj = new lbvserver();
		lbvserver_obj.set_name(name);
		lbvserver_obj.set_ipv46(ip);
		lbvserver_obj.set_port(port);
		lbvserver_obj.set_servicetype(type);
		lbvserver.add(ns_session,lbvserver_obj);

		} catch(Exception e) {
			System.out.println("Java Error -> " +e.getMessage());
			ret = false;
		}

		return ret;
	}


	private boolean	DelVserver(String name) 
	{
		boolean					ret = true;
		lbvserver			lbvserver_obj;

		try
		{
		lbvserver_obj = new lbvserver();
		lbvserver_obj.set_name(name);
		lbvserver.delete(ns_session,lbvserver_obj);

		} catch(Exception e) {
			System.out.println("Java Error -> " +e.getMessage());
			ret = false;
		}
		return		ret;
	}

	public boolean	AddDelServer(NSObject nsO)
	{
		boolean		ret = true;
		server	server_obj;

		try
		{
			server_obj	= new server();
			server_obj.set_ipaddress(nsO.ipAddr);
			server_obj.set_name(nsO.serverName);
			if(nsO.isDelete == false)
				server.add(ns_session,server_obj);
			else
				server.delete(ns_session,server_obj);

		} catch(Exception e) {
			ret = false;
		}

		return ret;
	}



	public boolean	AddDelHTTPService(NSObject nsO)
	{
		if(nsO.isDelete == false)
			return AddService(nsO.serviceName,nsO.serverName,nsO.port,"HTTP");
		else
			return	DelService(nsO);
	}

	public boolean	AddDelSSLService(NSObject nsO)
	{
		if(nsO.isDelete == false)
			return AddService(nsO.serviceName,nsO.serverName,nsO.port,"SSL");
		else
			return	DelService(nsO);
	}


	private boolean	AddService(String name,String server,int port,String type)
	{
		boolean		ret = true;
		service	service_obj;

		try
		{
			service_obj	= new service();
			service_obj.set_name(name);
			service_obj.set_servername(server);
			service_obj.set_port(port);
			service_obj.set_servicetype(type);
			service.add(ns_session,service_obj);
	
		} catch(Exception e) {
			ret = false;
		}

		return ret;
	}


	private boolean	DelService(NSObject nsO)
	{
		boolean		ret = true;
		service	service_obj;

		try
		{
			service_obj	= new service();
			service_obj.set_name(nsO.serviceName);
			service.delete(ns_session,service_obj);

		} catch(Exception e) {
			ret = false;
		}
		return ret;
	}


	private	boolean	BindUnbindCipher(NSObject nsO)
	{
		boolean		ret	= true;
		sslservice_sslcipher_binding		obj_2;
		sslvserver_sslciphersuite_binding	obj_3;

		try
		{
			if(nsO.isVserver == true)
			{
				obj_3 = new sslvserver_sslciphersuite_binding();
				obj_3.set_vservername(nsO.vserverName);
				obj_3.set_ciphername(nsO.cipherName);

				if(nsO.isUnbind)
					sslvserver_sslciphersuite_binding.delete(ns_session,obj_3);
				else
					sslvserver_sslciphersuite_binding.add(ns_session,obj_3);
			}
			else
			{
				obj_2 = new sslservice_sslcipher_binding();
				obj_2.set_servicename(nsO.serviceName);
				obj_2.set_ciphername(nsO.cipherName);

				if(nsO.isUnbind)
					sslservice_sslcipher_binding.delete(ns_session,obj_2);
				else
					sslservice_sslcipher_binding.add(ns_session,obj_2);
			}

		} catch(Exception e) {
            System.out.println("Java Error -> " +e.getMessage());
            ret = false;
        }

		return ret;
	}


	private	boolean	UnbindAllCipher(NSObject nsO)
	{
		boolean		ret	=	true;
		sslvserver_sslciphersuite_binding	sv[];
		sslservice_sslciphersuite_binding	sc[];
		
		try
		{
			if(nsO.isVserver == true)
			{
			sv	=	
			sslvserver_sslciphersuite_binding.get(ns_session,nsO.vserverName);
			sslvserver_sslciphersuite_binding.delete(ns_session,sv);
			}
			else
			{
			System.out.println("serviceName: " + nsO.serviceName);
			sc	=	
			sslservice_sslciphersuite_binding.get(ns_session,nsO.serviceName);
			for(sslservice_sslciphersuite_binding s:sc)
			{
				System.out.println(s.get_ciphername());
			}
			sslservice_sslciphersuite_binding.delete(ns_session,sc);
			}
		} catch(Exception e) {
            System.out.println("Java Error -> " +e.getMessage());
            ret = false;
        }
		return ret;	
	}



	private	boolean	BindUnbindService (NSObject nsO) throws Exception
	{
		boolean		ret = true;
		lbvserver_service_binding	obj;
		
		obj = new lbvserver_service_binding();
		obj.set_name(nsO.vserverName);
		obj.set_servicename(nsO.serviceName);

		if(nsO.isUnbind == true)
			lbvserver_service_binding.delete(ns_session,obj);
		else
			lbvserver_service_binding.add(ns_session,obj);

		return ret;
	}



	private	boolean	SetUnsetSSLVserver(NSObject nsO) throws Exception
	{
		boolean			ret = true;
		sslvserver		obj;

		obj		= new sslvserver();
		
		if(nsO.isSetClientAuth == true) 
		{
			if(nsO.clientAuthEnabled == true)
			{
				obj.set_clientauth("ENABLED");

				if(nsO.clientCertMandatory == true)
					obj.set_clientcert("MANDATORY");
				else
					obj.set_clientcert("OPTIONAL");
			}
			else
				obj.set_clientauth("DISABLED");
		}

		if(nsO.isSetSessTimeout == true)
			obj.set_sesstimeout(nsO.sessTimeout);

		if(nsO.isSetDH == true)
		{
			if(nsO.dhEnabled == true)
				obj.set_dh("ENABLED");
			else
				obj.set_dh("DISABLED");
		}

		if(nsO.isSetDHFile == true)
			obj.set_dhfile(nsO.dhFileName);

		if(nsO.isSetDHCount == true)
			obj.set_dhcount(nsO.dhCount);

		if(nsO.isSetERsa == true)
		{
			if(nsO.eRsaEnabled == true)
				obj.set_ersa("ENABLED");
			else
				obj.set_ersa("DISABLED");
		}

		if(nsO.isSetSNI == true)
		{
			if(nsO.sniEnabled == true)
				obj.set_snienable("ENABLED");
			else
				obj.set_snienable("DISABLED");
		}

		if(nsO.isSetCN == true)
		{
			if(nsO.CNEnabled == true)
				obj.set_sendclosenotify("YES");
			else
				obj.set_sendclosenotify("NO");
		}

		if(nsO.isSetSsl3 == true)
		{
			if(nsO.ssl3Enabled == true)
				obj.set_ssl3("ENABLED");
			else
				obj.set_ssl3("DISABLED");
		}
		if(nsO.isSetTls1 == true)
		{
			if(nsO.tls1Enabled == true)
				obj.set_tls1("ENABLED");
			else
				obj.set_tls1("DISABLED");
		}
		if(nsO.isSetTls11 == true)
		{
			if(nsO.tls11Enabled == true)
				obj.set_tls11("ENABLED");
			else
				obj.set_tls11("DISABLED");
		}
		if(nsO.isSetTls12 == true)
		{
			if(nsO.tls12Enabled == true)
				obj.set_tls12("ENABLED");
			else
				obj.set_tls12("DISABLED");
		}

		return ret;
	}


	public	boolean	Execute(NSObject nsO)
	{
		boolean		ret = true;

		try
		{
		switch(nsO.command)
		{
			case	NSCommand.Login :
					ret = Login(nsO.userName,nsO.passwd);
					System.out.println("Execute: Login returned " + ret);
					break;

			case	NSCommand.ADDDELMIP :
					{
					nsip	obj	=	new nsip();
					obj.set_ipaddress(nsO.ipAddr);
					obj.set_netmask(nsO.netMask);
					obj.set_type("SNIP");
					if(nsO.isDelete == true)
						obj.delete(ns_session,obj);
					else
						obj.add(ns_session,obj);
					}
					break;

			case	NSCommand.ADDDELVIP :
					{
					nsip	obj	=	new nsip();
					obj.set_ipaddress(nsO.ipAddr);
					obj.set_netmask(nsO.netMask);
					obj.set_type("VIP");
					if(nsO.isDelete == true)
						obj.delete(ns_session,obj);
					else
						obj.add(ns_session,obj);
					}
					break;

			case	NSCommand.AddDelHTTPVserver :
					ret = AddDelHTTPVserver(nsO);
					break;

			case	NSCommand.AddDelSSLVserver :
					ret = AddDelSSLVserver(nsO);
					break;

			case	NSCommand.AddDelServer :
					ret = AddDelServer(nsO);
					break;

			case	NSCommand.AddDelHTTPService :
					ret = AddDelHTTPService(nsO);
					break;

			case	NSCommand.AddDelSSLService :
					ret = AddDelSSLService(nsO);
					break;

			case	NSCommand.AddDelCertKey :
					ret = AddDelCertKey(nsO);
					break;

			case	NSCommand.BindUnbindCertKey :
					ret = BindUnbindCertKey(nsO); 
					break;

			case	NSCommand.BindUnbindCipher :
					ret = BindUnbindCipher(nsO); 
					break;

			case	NSCommand.UnbindAllCipher :
					ret = UnbindAllCipher(nsO); 
					break;

			case	NSCommand.BindUnbindService :
					ret = BindUnbindService(nsO); 
					break;

			case	NSCommand.SetUnsetLBVserver :
					break;

			case	NSCommand.SetUnsetSSLVserver :
					SetUnsetSSLVserver(nsO);
					break;

			case	NSCommand.SetUnsetService :
					break;

			case	NSCommand.SetUnsetSSLService :
					break;

			default :
					ret = false;
					break;
		}
		} catch (Exception e) {
			ret = false;
			System.out.println("Exception : " + e.getMessage() + " Command " + nsO.command);
		}

		return ret;
	}



	public static void main(String[] args) 
	{
		lbvserver						lbvserver_obj;
		sslcertkey						sslcertkey_obj;
		sslvserver_sslcertkey_binding	sslvserver_sslcertkey_binding_obj;
		sslservice_sslcertkey_binding	sslservice_sslcertkey_binding_obj;
		service							service_obj;
		server							server_obj;
		sslcipher_sslvserver_binding	sslcipher_sslvserver_binding_obj;
		sslvserver_sslcipher_binding	sslvserver_sslcipher_binding_obj;
		lbvserver_service_binding		lbvserver_service_binding_obj;
		sslvserver						sslvserver_obj;
		ServerSocket					Ssock;
		Socket							Sock;
		InputStream						inS;
		OutputStream					ouS;
		InputStreamReader				isR;
		Gson							gson;
		String							jstring;
		byte							B[];


		try {
	
			//Ssock = new ServerSocket(8090);
			//Sock = Ssock.accept();
			//inS = Sock.getInputStream();
			//ouS = Sock.getOutputStream();
			//isR = new InputStreamReader(inS);
			//System.out.println("Creating NitroC\n");
			//System.out.println(args[0]);
			//System.out.println(args[1]);
			//System.out.println("Integer: " + Integer.parseInt(args[2]));
			//System.out.println(args[2]);


			NitroC	nitroC = new NitroC(args[0],80,Integer.parseInt(args[1]));
			nitroC.Listen();


			//System.out.println("Code started");
			//nitro_service ns_session = 
			//new nitro_service("10.102.28.133","HTTP");
			//ns_session.login("nsroot","nsroot");
			//sslvserver_sslcertkey_binding  obj1;			
			//obj1 = new sslvserver_sslcertkey_binding();
			//obj1.set_certkeyname("server_one");
			//obj1.set_vservername("v1");
			//sslvserver_sslcertkey_binding.add(ns_session,obj1);
			//obj1.perform_operation(ns_session);


			//nitro_service ns_session = 
			//	new nitro_service("10.102.28.133","HTTP");
			//ns_session.login("nsroot","nsroot");
			//sslvserver_sslciphersuite_binding sc[];
			//sc = sslvserver_sslciphersuite_binding.get(ns_session,"v1");
			//System.out.println("Total cipher bindings: " + sc.length);
			//for(sslvserver_sslciphersuite_binding s: sc)
			//{
			//	System.out.println(s.get_ciphername());
			//}
			//gson = new GsonBuilder().create();
			//String gStr = gson.toJson(sc);
			//System.out.println(gStr);
			//sslvserver_sslciphersuite_binding.delete(ns_session,sc);

		} catch(Exception e) {
			System.out.println("Java Error -> " +e.getMessage());
		}
	}

}
