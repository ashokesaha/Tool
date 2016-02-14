import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.io.*;
import java.net.*;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;


public	class	SSLIface 
{
	static	int			MAXJOBJECTS	= 8;

	ArrayList<JObject>		jO;
	ArrayList<Socket>		Peer;

	SSLIface() {
		jO		= new ArrayList<JObject>();
		Peer	= new ArrayList<Socket>();
	}


	public	boolean		AddPeer(String Host, int port) {
		boolean		ret = true;
		Socket		sock;
		JObject		jo;

		try
		{
			sock	= new Socket(Host,port);
			jo		= new JObject();
			Peer.add(sock);
			jO.add(jo);

		} catch (IOException ioe) {
			sock = null;
			ret	= false;
			System.out.println("Socket error: " + ioe.getMessage());
		} catch (SecurityException	se) {
			sock = null;
			ret	= false;
			System.out.println("Socket error: " + se.getMessage());
		}
		return ret;
	}


	public	int		PeerCount() {
		return	Peer.size();	
	}


	public	JObject	GetJO(int index) {
		JObject	jo = null;

		if(index < PeerCount())
			jo = jO.get(index);

		return	jo;
	}


	public	int		Command() {
		InputStream		inS;
		OutputStream	outS;
		JObject			jo;
		Socket			sock;
		String			jstr;
		int				index,count=0;

		for(index = 0; index < Peer.size(); index++)
		{
			sock	=	Peer.get(index);
			jo		=	jO.get(index);
			jstr	=	jo.toString();

			try
			{
				System.out.println("jstr: " + jstr);
				outS	=	sock.getOutputStream();
				outS.write(jstr.getBytes());
			} catch(IOException	ioe) {
				continue;
			}
			count++;
		}
		return count;
	}


	public	static	void	main(String argc[])
	{
		int			count;
		boolean		ret = false;

		SSLIface	iface = new SSLIface();
		ret = iface.AddPeer("10.102.28.61",2345);
		if(ret == false)
		{
			System.out.println("Add Peer failed\n");
			return;
		}

		count		= iface.PeerCount();
		JObject		jO = iface.GetJO(0);
		jO.setDUT("10.102.28.236",443);
		iface.Command();
	}


}


class	JObject	
{
	String	ip;
	String	log;
	String	cert;
	String	key;
	String	version;
	String	cipher;
	int		port;
	int		reuse;
	int		reneg;
	int		timeout;
	int		ckv;
	int		print;
	int		iter;
	int		err;
	int		loop;
	int		burst;
	int		padtest;
	int		adminport;
	int		inetd;
	String	message;
	int		nitrotest;

	JObject()	{
		timeout		= 100;
		loop		= 1;
		burst		= 1;
		log			= new String("log.out");
		//message		= new String("Test Message");
	}

	public	String	toString() {
		Gson	gson;
		String	gStr;

		gson	= new GsonBuilder().create();
		gStr	= gson.toJson(this);
		return	gStr;
	}

	public	void	setDUT(String ip, int port)	{
		this.ip		= ip;
		this.port	= port;
	}

}

