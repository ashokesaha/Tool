#include <stdio.h>
#include <string.h>
#include "hashdef.h"
#include "nitro_lib.h"


cJSON	*javaLogin(char *username,char *passwd)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JLogin);
	cJSON_AddStringToObject(obj1,"userName",username);
	cJSON_AddStringToObject(obj1,"passwd",passwd);
	return obj1;
}


cJSON	*javaAddHTTPVserver(char *vservername,char *ip,int port)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JAddHTTPVserver);
	cJSON_AddStringToObject(obj1,"vserverName",vservername);
	cJSON_AddStringToObject(obj1,"ipAddr",ip);
	cJSON_AddNumberToObject(obj1,"port",port);
	return obj1;
}

cJSON	*javaAddSSLVserver(char *vservername,char *ip,int port)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JAddSSLVserver);
	cJSON_AddStringToObject(obj1,"vserverName",vservername);
	cJSON_AddStringToObject(obj1,"ipAddr",ip);
	cJSON_AddNumberToObject(obj1,"port",port);
	return obj1;
}

cJSON	*javaDelVserver(char *vservername)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JDelHTTPVserver);
	cJSON_AddStringToObject(obj1,"vserverName",vservername);
	return obj1;
}

cJSON	*javaAddHTTPService(char *service,char *server,int port)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JAddHTTPService);
	cJSON_AddStringToObject(obj1,"serviceName",service);
	cJSON_AddStringToObject(obj1,"serverName",server);
	cJSON_AddNumberToObject(obj1,"port",port);
	return obj1;
}

cJSON	*javaDelHTTPService(char *service)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JDelHTTPService);
	cJSON_AddStringToObject(obj1,"serviceName",service);
	return obj1;
}

cJSON	*javaAddSSLService(char *service,char *server,int port)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JAddSSLService);
	cJSON_AddStringToObject(obj1,"serviceName",service);
	cJSON_AddStringToObject(obj1,"serverName",server);
	cJSON_AddNumberToObject(obj1,"port",port);
	return obj1;
}

cJSON	*javaDelSSLService(char *service)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JDelSSLService);
	cJSON_AddStringToObject(obj1,"serviceName",service);
	return obj1;
}




cJSON	*javaAddServer(char *servername,char *ip)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JAddServer);
	cJSON_AddStringToObject(obj1,"serverName",servername);
	cJSON_AddStringToObject(obj1,"ipAddr",ip);
	return obj1;
}

cJSON	*javaDelServer(char *servername)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JDelServer);
	cJSON_AddStringToObject(obj1,"serverName",servername);
	return obj1;
}

cJSON	*javaAddCertKey(char *certkeyname,char *certfile,char *keyfile)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JAddCertKey);
	cJSON_AddStringToObject(obj1,"certKeyName",certkeyname);
	cJSON_AddStringToObject(obj1,"certFileName",certfile);
	cJSON_AddStringToObject(obj1,"keyFileName",keyfile);
	return obj1;
}

cJSON	*javaDelCertKey(char *certkeyname)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JDelCertKey);
	cJSON_AddStringToObject(obj1,"certKeyName",certkeyname);
	return obj1;
}



cJSON	*javaBindUnbindCipher(char *servicename,char *ciphername,int isvserver,int isunbind)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JBindUnbindCipher);

	if(isvserver)
		cJSON_AddStringToObject(obj1,"vserverName",servicename);
	else
		cJSON_AddStringToObject(obj1,"serviceName",servicename);

	cJSON_AddStringToObject(obj1,"cipherName",ciphername);

	if(isvserver)
		cJSON_AddTrueToObject(obj1,"isVserver");
	if(isunbind)
		cJSON_AddTrueToObject(obj1,"isUnbind");

	return obj1;
}



cJSON	*javaUnbindAllCipher(char *servicename,int isvserver)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JUnbindAllCipher);

	if(isvserver)
		cJSON_AddTrueToObject(obj1,"isVserver");

	if(isvserver)
		cJSON_AddStringToObject(obj1,"vserverName",servicename);
	else
		cJSON_AddStringToObject(obj1,"serviceName",servicename);

	return obj1;
}



cJSON	*javaBindUnbindCertKey(char *servicename,char *certkeyname,int isvserver,int issni, int iscacert, int isunbind)
{
	cJSON	*obj1;

	obj1	= cJSON_CreateObject();
	cJSON_AddNumberToObject(obj1,"command",JBindUnbindrCertkey);
	if(isvserver)
		cJSON_AddStringToObject(obj1,"vserverName",servicename);
	else
		cJSON_AddStringToObject(obj1,"serviceName",servicename);

	cJSON_AddStringToObject(obj1,"certKeyName",certkeyname);

	if(issni)
		cJSON_AddTrueToObject(obj1,"isSNICert");
	if(iscacert)
		cJSON_AddTrueToObject(obj1,"isCACert");
	if(isunbind)
		cJSON_AddTrueToObject(obj1,"isUnbind");
	if(isvserver)
		cJSON_AddTrueToObject(obj1,"isVserver");
		
	return obj1;
}


int		jsonSendRecv(cJSON *json,int sock)
{
	char	*str;
	char	buf[64];
	int		len;

	str = cJSON_PrintUnformatted(json);
	len = send(sock,str,strlen(str),0);
	len = send(sock,"\n",strlen("\n"),0);
	printf("sent (%d) [%s]\n",len,str);

	len = recv(sock,buf,32,0);
	printf("received (%d)  [%s]\n", len, buf);
	json = cJSON_Parse(buf);
	json = cJSON_GetObjectItem(json,"result");
	printf("result %d\n",json->valueint);
	return json->valueint;
}
