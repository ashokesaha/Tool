#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include "myHTTP.h"


int	HEXTODECIMAL(c)
{
	switch(c)
	{
		case '0':
		case '1':
		case '2':
		case '3':
		case '4':
		case '5':
		case '6':
		case '7':
		case '8':
		case '9': return (c - '0');
		case 'a':
		case 'b':
		case 'c':
		case 'd':
		case 'e':
		case 'f': return (c - 'a' + 10);
		case 'A':
		case 'B':
		case 'C':
		case 'D':
		case 'E':
		case 'F': return (c - 'A' + 10);
	}
	return 0;
}



char	CODETOCHAR(int val)
{
	int	c = 0;
	switch(val)
	{
		case 32 : c = ' '; break;
		case 33 : c = '!'; break;
		case 34 : c = '"'; break;
		case 35 : c = '#'; break;
		case 36 : c = '$'; break;
		case 37 : c = '%'; break;
		case 38 : c = '&'; break;
		case 39 : c = '\''; break;
		case 40 : c = '('; break;
		case 41 : c = ')'; break;
		case 42 : c = '*'; break;
		case 43 : c = '+'; break;
		case 44 : c = ','; break;
		case 45 : c = '-'; break;
		case 46 : c = '.'; break;
		case 47 : c = '/'; break;
		case 91 : c = '['; break;
		case 92 : c = '\\'; break;
		case 93 : c = ']'; break;
		case 94 : c = '^'; break;
		case 95 : c = '_'; break;
		case 96 : c = '`'; break;
		case 123: c = '{'; break;
		case 124: c = '|'; break;
		case 125: c = '}'; break;
		default : c = (char)val; break;
	}
	return c;
}

int URLDECODE(char * in, int inlen, char *out)
{
	char	*p = in, c;
	int		len = 0,val,err=0;

	while((c = *p++) && inlen)
	{
		switch(c)
		{
			case '%':
				if(inlen < 2) {err=-1;goto errlabel;}
				val = (HEXTODECIMAL(p[0]) * 16) + HEXTODECIMAL(p[1]);
				*out++ = CODETOCHAR(val);
				len++;
				inlen -= 2;
				p += 2;
				break;

			case '+':
				*out++ = ' ';
				len++;
				inlen--;
				break;
			
			default:
				*out++ = c;
				len++;
				inlen--;
				break;
		}
	}

errlabel:

	return len;
}


HTTP_CTX	*Login(char *username,char *passwd,char *host)
{
	HTTP_CTX	*ctx = NULL;
	char		buf[8192];
	char		jbuf[8192];
	char		jbufU[8192];
	char		*ptr;
	int			ret = 0;

	ctx = (HTTP_CTX *)malloc(sizeof(HTTP_CTX));
	ctx->username = strdup(username);
	ctx->passwd = strdup(passwd);
	ctx->host = strdup(host);
	ctx->sockfd = MakeSocket(host,80);
	if(!ctx->sockfd)
	{
		free(ctx);
		return NULL;
	}
	ctx->req = newLoginObject(username,passwd);
	if(!ctx->req)
	{
		free(ctx);
		return NULL;
	}
	ctx->req->jbuf = cJSON_PrintUnformatted(ctx->req);
	strcpy(jbuf,"object=");
	strcat(jbuf,cJSON_PrintUnformatted(ctx->req));

	printf("Login Json (%d): %s\n",strlen(jbuf),jbuf);

	ret = URLENCODE(jbuf,strlen(jbuf),jbufU);
	printf("URLENCIDED Login Json: %s\n",jbufU);
	printf("\n");

	sprintf(buf,LOGINSTR,host,ret);
	strcat(buf,jbufU);

	ret = send(ctx->sockfd,buf,strlen(buf),0);
	printf("sending login data (%d/%d)\n", ret,strlen(buf));
	printf("%s\n",buf);

	/* Tmp code to read response */
	sleep(2);
	ret = recv(ctx->sockfd,buf,4096,MSG_DONTWAIT);
	printf("received response (%d) :\n",ret);
	printf("%s\n",buf);

	return ctx;
}



cJSON	*newLoginObject(char *username,char *passwd)
{
	cJSON	*obj1,*obj2;

	obj1	= cJSON_CreateObject();
	obj2	= cJSON_CreateObject();
	cJSON_AddStringToObject(obj2,"username",username);
	cJSON_AddStringToObject(obj2,"password",passwd);
	cJSON_AddItemToObject(obj1,"login",obj2);
	//obj1->string = "object";
	return obj1;
}


int URLENCODE(char * in, int inlen, char *out)
{
	int		i;
	char	*ptr = out;
	
	for(i=0;i<inlen;i++)
		CHARTOCODE(in[i],out);
	return (out - ptr);
}


int	MakeSocket(char *ip,int port)
{
	int		ret;
	int		sd;
	struct	sockaddr_in	addr;

	sd = socket(PF_INET,SOCK_STREAM,6);
	bzero(&addr,sizeof(addr));
	addr.sin_family	=	PF_INET;
	addr.sin_port	=	htons(port);
	addr.sin_addr.s_addr =  inet_addr(ip);
	addr.sin_len	= sizeof(addr);

	ret = connect(sd,(struct sockaddr *)&addr,sizeof(addr));

	if(ret < 0)
		return -1;
	return sd;
}



#ifdef	SELFTEST
main()
{
	char		out[1024];
	int			len;
	HTTP_CTX	*ctx;

	ctx = Login("nsroot","nsroot","10.102.28.133");
}

#endif
