import java.util.Arrays;
import java.util.List;

import com.citrix.netscaler.nitro.exception.nitro_exception;
import com.citrix.netscaler.nitro.resource.config.lb.lbvserver;
import com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey;
import com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding;
import com.citrix.netscaler.nitro.resource.config.ssl.sslservice_sslcertkey_binding;
import com.citrix.netscaler.nitro.service.nitro_service;
import com.citrix.netscaler.nitro.resource.config.basic.service;
import com.citrix.netscaler.nitro.resource.config.basic.server;
import com.citrix.netscaler.nitro.resource.config.ssl.sslcipher_sslvserver_binding;
import com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcipher_binding;
import com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding;
import com.citrix.netscaler.nitro.resource.config.ssl.sslvserver;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.*;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;


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


	public void NitroC(String dutIP,int dutPort,int listenPort)
	{
		this.dutIP		= dutIP;
		this.dutPort	= dutPort;
		this.listenPort	= listenPort;
		this.isListen	= false;
		this.isTerminate	= false;
	}

	public boolean Login(String userName,String passwd)
	{
		if(ns_session.isLogin() == true)
			return ns_session.isLogin();

		try
		{
			nitro_service ns_session = 
				new nitro_service(this.dutIP,"HTTP");
			ns_session.login(userName,passwd);

		} catch (nitro_exception e) {
			;
		} catch (Exception e) {
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
		Gson							gson;
		String							jstring;

		if(isListen == true)
			return isListen;

		gson = new GsonBuilder().create();

		while (isTerminate == false)
		{
			try 
			{
				isListen	= true;
				Ssock		= new ServerSocket(this.listenPort);
				Sock		= Ssock.accept();
				inS			= Sock.getInputStream();
				ouS			= Sock.getOutputStream();
				isR			= new InputStreamReader(inS);

				nsO			= gson.fromJson(isR, NSObject.class);
				Execute(nsO);

			} catch (IOException ioe) {
				isListen = false;
			}
		}

		//Close sockets and streams

		return isListen;
	}


	public int	AddHTTPVserver(NSObject nsO)
	{
		return AddVserver(nsO.vserverName,nsO.ipAddr,nsO.port, "HTTP"); 
	}
	public int	AddSSLVserver(NSObject nsO) 
	{
		return AddVserver(nsO.vserverName,nsO.ipAddr,nsO.port, "SSL"); 
	}

	private int	AddVserver(String name, String ip, int port,String type) 
	{
		int					ret = 0;
		lbvserver			lbvserver_obj;

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
			ret = -1;
		}

		return ret;
	}


	private int	DelVserver(String name) 
	{
		int					ret = 0;
		lbvserver			lbvserver_obj;

		try
		{
		lbvserver_obj = new lbvserver();
		lbvserver_obj.set_name(name);
		lbvserver.delete(ns_session,lbvserver_obj);

		} catch(Exception e) {
			System.out.println("Java Error -> " +e.getMessage());
			ret = -1;
		}
		return		ret;
	}

	public int	AddDelServer(NSObject nsO,boolean add)
	{
		int		ret = 0;
		server	server_obj;

		try
		{
			server_obj	= new server();
			server_obj.set_ipaddress(nsO.ipAddr);
			server_obj.set_name(nsO.serverName);
			if(add == true)
				server.add(ns_session,server_obj);
			else
				server.delete(ns_session,server_obj);

		} catch(Exception e) {
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
			service_obj	= new service();
			service_obj.set_name(name);
			service_obj.set_servername(server);
			service_obj.set_port(port);
			service_obj.set_servicetype(type);
			service.add(ns_session,service_obj);
	
		} catch(Exception e) {
			ret = -1;
		}

		return ret;
	}


	private int	DelService(NSObject nsO)
	{
		int		ret = 0;
		service	service_obj;

		try
		{
			service_obj	= new service();
			service_obj.set_name(nsO.serviceName);
			service.delete(ns_session,service_obj);

		} catch(Exception e) {
			ret = -1;
		}
		return ret;
	}




	public	int	Execute(NSObject nsO)
	{
		int		ret = 0;
		switch(nsO.command)
		{
			case	NSCommand.AddHTTPVserver :
					ret = AddHTTPVserver(nsO);
					break;

			case	NSCommand.AddSSLVserver :
					ret = AddSSLVserver(nsO);
					break;

			case	NSCommand.DelHTTPVserver :
			case	NSCommand.DelSSLVserver :
					ret = DelVserver(nsO.vserverName);
					break;

			case	NSCommand.AddServer :
					ret = AddDelServer(nsO,true);
					break;

			case	NSCommand.DelServer :
					ret = AddDelServer(nsO,false);
					break;

			case	NSCommand.AddHTTPService :
					ret = AddHTTPService(nsO);
					break;

			case	NSCommand.AddSSLService :
					ret = AddSSLService(nsO);
					break;

			case	NSCommand.DelHTTPService :
			case	NSCommand.DelSSLService :
					ret = DelService(nsO);
					break;

			default :
					ret = -1;
					break;
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

		try {
	
			Ssock = new ServerSocket(8090);
			Sock = Ssock.accept();
			inS = Sock.getInputStream();
			ouS = Sock.getOutputStream();
			isR = new InputStreamReader(inS);

			gson = new GsonBuilder().create();
			jstring="{name:\"ashoke\",age:100,address:\"Ajmera Green acres\"}";
			Person p = gson.fromJson(isR, Person.class);
			System.out.println(p);

			nitro_service ns_session = 
					new nitro_service("10.102.28.133","HTTP");

			ns_session.login("nsroot","nsroot");

		} catch (IOException ioe) {

		} catch(nitro_exception error) {
			System.out.println("NITRO Error -> Code " + error.getErrorCode() +
												" : " +error.getMessage());
		} catch(Exception e) {
			System.out.println("Java Error -> " +e.getMessage());
		}
	}

}




class	NSCommand {

	static final int AddHTTPVserver = 101;
	static final int DelHTTPVserver = 102;
	static final int AddSSLVserver = 103;
	static final int DelSSLVserver = 104;

	static final int AddHTTPService = 105;
	static final int DelHTTPService = 106;
	static final int AddSSLService = 107;
	static final int DelSSLService = 108;

	static final int AddCertKey = 109;
	static final int DelCertKey = 110;

	static final int BindSSLVserverCertkey = 111;
	static final int UnbindSSLVserverCertkey = 112;
	static final int BindSSLServiceCertkey = 113;
	static final int UnbindSSLServiceCertkey = 114;

	static final int BindSSLVserverCACertkey = 115;
	static final int UnbindSSLVserverCACertkey = 116;
	static final int BindSSLServiceCACertkey = 117;
	static final int UnbindSSLServiceCACertkey = 118;

	static final int BindSSLVserverSNICertkey = 119;
	static final int UnbindSSLVserverSNICertkey = 120;
	static final int BindSSLServiceSNICertkey = 121;
	static final int UnbindSSLServiceSNICertkey = 122;

	static final int BindSSLVserverCipher = 123;
	static final int UnbindSSLVserverCipher = 124;
	static final int BindSSLServiceCipher = 124;
	static final int UnbindSSLServiceCipher = 125;

	static final int EnableSSLVserverCauth = 126;
	static final int DisableSSLVserverCauth = 127;
	static final int EnableSSLServiceCauth = 128;
	static final int DisableSSLServiceCauth = 129;

	static final int EnableSSLVserverSessReuse = 130;
	static final int DisableSSLVserverSessReuse = 131;
	static final int EnableSSLServiceSessReuse = 132;
	static final int DisableSSLServiceSessReuse = 133;

	static final int EnableSSLVserverDH = 134;
	static final int DisableSSLVserverDH = 135;
	static final int EnableSSLServiceDH = 136;
	static final int DisableSSLServiceDH = 137;

	static final int SetSSLVserverSessionTimeout = 138;
	static final int SetSSLServiceSessionTimeout = 139;

	static final int EnableSSLVserverVersion = 140;
	static final int DisableSSLVserverVersion = 141;
	static final int EnableSSLServiceVersion = 142;
	static final int DisableSSLServiceVersion = 143;

	static final int AddCRL = 144;
	static final int DelCRL = 145;

	static final int AddOCSPResponder = 146;
	static final int DelOCSPResponder = 147;

	static final int AddServer = 148;
	static final int DelServer = 149;
}



class	NSObject	{
	int			command;

	boolean		isVserver;
	boolean		isCACert;

	int			version; //0=SSLv3,1=tls1.0,2=tls1.1,3=tls1.2
	int			sessTimeout;
	int			port;

	String		vserverName;
	String		serviceName;
	String		cipherName;
	String		certKeyName;
	String		certFileName;
	String		keyFileName;
	String		ocspName;
	String		crlName;
	String		dhfileName;
	String		serverName;
	String		ipAddr;
}



class Person {
	private String  name;
	private int  	age;
	private String  address;

	Person()
	{
	}

	Person(String name,int age,String address)
	{
		this.name = name;
		this.age = age;
		this.address = address;
	}

	public String toString()
	{
		String str = "Name: " + name + " Age: " + age + " Address: " + address;
		return str;
	}
}
