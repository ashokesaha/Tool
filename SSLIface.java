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
		int		count;
		boolean		ret = false;
		TestHarness	tH;
		NitroC		nC;
		NSVIP		vIP;
		NSLBVSERVER	vsrvr;

		tH = TestHarness.getTestHarness();
		tH.ConnectToDUT("10.102.28.133",80,"nsroot","nsroot");
		nC	= tH.getDUT();

		vIP	= new NSVIP("172.16.10.1");
		vsrvr	= new NSLBVSERVER(vIP.getIP(),80,"vserver-1");
		vsrvr.Delete();
		vIP.Delete();
	}


}
