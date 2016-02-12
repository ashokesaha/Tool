#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/errno.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include "Entities.h"
#include "myHTTP.h"
#include "hashdef.h"
#include "cJSON.h"


cJSON	*ReadResponse(HTTP_CTX *ctx);
cJSON	*newVserverObject(HTTP_CTX *,char *,char *,int ,char *);
cJSON	*javaLogin(char *username,char *passwd);
cJSON	*javaAddHTTPVserver(char *vservername,char *ip,int port);
cJSON	*javaAddSSLVserver(char *vservername,char *ip,int port);
cJSON	*javaDelVserver(char *vservername);
cJSON	*javaAddHTTPService(char *service,char *server,int port);
cJSON	*javaDelHTTPService(char *service);
cJSON	*javaAddSSLService(char *service,char *server,int port);
cJSON	*javaDelSSLService(char *service);
cJSON	*javaAddServer(char *servername,char *ip);
cJSON	*javaDelServer(char *servername);
int		jsonSendRecv(cJSON *json,int sock);



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
	cJSON		*jsn;
	char		buf[8192];
	char		jbuf[8192];
	char		jbufU[8192];
	char		*ptr;
	int			ret = 0;

	ctx = (HTTP_CTX *)malloc(sizeof(HTTP_CTX));
	ctx->rState = resp_init;
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

	ret = URLENCODE(jbuf,strlen(jbuf),jbufU);

	sprintf(buf,LOGINSTR,host,ret);
	strcat(buf,jbufU);

	ret = send(ctx->sockfd,buf,strlen(buf),0);

	allocReadBuf(ctx);
	jsn = ReadResponse(ctx);
	if(jsn)
	{
		char	*jstr;

		jstr = cJSON_GetObjectItem(jsn,"sessionid")->valuestring;
		ctx->sessid = strdup(jstr);
		printf("\n\nsess: %s\n",jstr);
	}

	return ctx;
}


int		AddVserver(HTTP_CTX *ctx,char *name,char *ip,int port, char *type)
{
	cJSON		*jsn;
	char		jbuf[8192];
	char		jbufU[8192];
	int			ret = 0;
	int			len = 0;

	jsn	= newVserverObject(ctx,name,ip,port,type);
	if(!jsn)
		return -1;

	strcpy(jbuf,"object=");
	strcat(jbuf,cJSON_PrintUnformatted(jsn));
	ret = URLENCODE(jbuf,strlen(jbuf),jbufU);

	sprintf(jbuf,LOGINSTR,ip,ret);
	strcat(jbuf,jbufU);
	printf("%s: request :\n%s\n",__FUNCTION__,jbuf);

	ret = 0;
	len = 0;
	while(len < strlen(jbuf))
	{
		ret = send(ctx->sockfd,jbuf+len,strlen(jbuf)-len,0);
		if(ret <= 0)
			break;
		len += ret;
	}
	if(len != strlen(jbuf))
		return -1;

	jsn = ReadResponse(ctx);
	if(jsn)
	{
		char	*jstr;
		jstr = cJSON_PrintUnformatted(jsn);
		printf("%s: response :\n%s\n",__FUNCTION__,jstr);
	}
	return 0;
}


int		allocReadBuf(HTTP_CTX *ctx)
{

	ctx->readBuf[0].ptr = malloc(MAXHDRSIZE);
	ctx->readBuf[0].len = 0;
	return 0;
}


int		freeReadBuf(HTTP_CTX *ctx)
{
	int		i;

	free(ctx->readBuf[0].ptr);
	ctx->readBuf[0].ptr = NULL;
	ctx->readBuf[0].len = 0;

	free(ctx->readBuf[1].ptr);
	ctx->readBuf[1].ptr = NULL;
	ctx->readBuf[1].len = 0;

	return 0;
}

cJSON	*newLoginObject(char *username,char *passwd)
{
	cJSON	*obj1,*obj2;

	obj1	= cJSON_CreateObject();
	obj2	= cJSON_CreateObject();
	cJSON_AddStringToObject(obj2,"username",username);
	cJSON_AddStringToObject(obj2,"password",passwd);
	cJSON_AddItemToObject(obj1,"login",obj2);
	return obj1;
}



cJSON	*newVserverObject(HTTP_CTX *ctx,char *name,char *ip,int port,char *type)
{
	cJSON	*obj1,*obj2;
	obj1	= cJSON_CreateObject();
	obj2	= cJSON_CreateObject();

	cJSON_AddStringToObject(obj2,"name",name);
	cJSON_AddStringToObject(obj2,"servicetype",type);
	cJSON_AddStringToObject(obj2,"ipv46",ip);
	cJSON_AddNumberToObject(obj2,"port",port);

	cJSON_AddStringToObject(obj1,"sessionid",ctx->sessid);
	cJSON_AddItemToObject(obj1,"lbvserver",obj2);
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
	{
		perror("connect:");
		return -1;
	}
	return sd;
}


/* Status-Line = HTTP-Version SP Status-Code SP Reason-Phrase CRLF */
int		ReadStatus(HTTP_CTX	*ctx)
{
	int		ret;

	do
	{
		/* Eevry time we read, the lastOff is the amount we 
		 * did not process in last iteration. So, parsing should
		 * happen from the beginning of the buffer and the length
		 * is lastOff + ret
		 */
		ret	= recv(ctx->sockfd,ctx->readBuf[0].ptr+ctx->lastOff,
							MAXSTATUSSIZE - ctx->lastOff, MSG_DONTWAIT);

		if(ret <= 0  &&  errno != EAGAIN)
			break;
		if(ret == -1  &&  errno == EAGAIN)
			continue;

		ParseRespStatus(ctx,ret+ctx->lastOff);

		/* Whenever we come out of parsing, the unprocessed data (can
		 * be part of status line, or part of header ... is already
		 * copied to the start of the buffer and lastOff is set
		 * accordingly.
		 */
			
		if(ctx->rState != resp_status)
			break;

		//ctx->lastOff += ret;

	} while (ret == -1 &&  errno == EAGAIN && ctx->lastOff < MAXSTATUSSIZE);

	return ctx->rState;
}


/* Everytime we enter this function, the data to be processed is from
 * the start of the buffer. Pending data from last iteration
 * that we could not process were copied at the front and more data
 * read. The chkpt is the last processed data
 */
int	ParseRespStatus(HTTP_CTX *ctx, int len)
{
	int		i;
	char	*p = ctx->readBuf[0].ptr;
	char	*chkpt = NULL;

	for(i=0; i<len; i++)
	{
		if(ctx->Status.substatus == STATUS_DONE)
		{
			strncpy(p,&p[i],len-i);
			ctx->lastOff = len - i;
			break;
		}

		switch(ctx->Status.substatus)
		{
			case	STATUS_START:	
				if(p[i]==SP  ||  p[i]==CR  ||  p[i]==LF)
					goto status_err;
				ctx->Status.version = NULL;
				ctx->Status.status = NULL;
				ctx->Status.reason = NULL;
				ctx->Status.substatus = STATUS_VER;

			case	STATUS_VER:	
				if(ctx->Status.version == NULL)
					ctx->Status.version = &p[i];
				if(p[i]==CR  ||  p[i]==LF)
					goto status_err;
				if(p[i] == SP)
				{
					p[i] = 0;
					ctx->Status.version = strdup(ctx->Status.version);
					ctx->Status.substatus = STATUS_CODE;
					chkpt = &p[i+1];
				}
				break;

			case	STATUS_CODE:	
				if(ctx->Status.status == NULL)
					ctx->Status.status = &p[i];
				if(p[i]==CR  ||  p[i]==LF)
					goto status_err;
				if(p[i] == SP)
				{
					p[i] = 0;
					ctx->Status.status = strdup(ctx->Status.status);
					ctx->Status.substatus = STATUS_REASN;
					chkpt = &p[i+1];
				}
				break;

			case	STATUS_REASN:	
				if(p[i] == LF)
					goto status_err;
				if(ctx->Status.reason == NULL)
					ctx->Status.reason = &p[i];
				if(p[i] == CR)
					ctx->Status.substatus = STATUS_LF;
				break;
		
			case	STATUS_LF:	
				if(p[i] != LF)
					goto status_err;
				ctx->Status.substatus = STATUS_DONE;
				ctx->rState = resp_header;
				break;
		}
	}

	if((ctx->Status.substatus != STATUS_DONE) && chkpt) 
	{
		strncpy(p,chkpt,len - (chkpt - p));
		ctx->lastOff = len - (chkpt - p);
	}

status_err:
	return ctx->Status.substatus;
}



int		ReadHeader(HTTP_CTX	*ctx)
{
	int		ret;
	do
	{
		ret	= recv(ctx->sockfd,ctx->readBuf[0].ptr+ctx->lastOff,
							MAXHDRSIZE - ctx->lastOff, MSG_DONTWAIT);

		if(ret <= 0  &&  errno != EAGAIN)
			break;
		if(ret == -1  &&  errno == EAGAIN)
			continue;

		ParseRespHeader(ctx, ret + ctx->lastOff);
			
		if(ctx->rState != resp_header)
			break;

	} while (ret == -1 &&  errno == EAGAIN && ctx->lastOff < MAXHDRSIZE);

	return ctx->rState;
}



int	ParseRespHeader(HTTP_CTX *ctx, int len)
{
	int		i,j;
	char	*p = ctx->readBuf[0].ptr;
	char	*chkpt = NULL;

	for(i=0; i<len; i++)
	{
		if(ctx->Header.substatus == HEADER_DONE_CRLF)
		{
			strncpy(p,&p[i],len-i);
			ctx->lastOff = len - i;
			ctx->rState = resp_body;
			break;
		}

		switch(ctx->Header.substatus)
		{
			case	HEADER_START:	
				if(p[i]==SP  ||  p[i]==CR  ||  p[i]==LF)
					goto header_err;

				ctx->Header.nameValNum = 64;	
				ctx->Header.curNum = 0;	
				ctx->Header.nameVal = (NAMEVAL *)malloc(sizeof(NAMEVAL) * ctx->Header.nameValNum);
				for(j=0; j < ctx->Header.nameValNum; j++)
				{
					ctx->Header.nameVal[j].name = NULL;
					ctx->Header.nameVal[j].value = NULL;
				}

				ctx->Header.substatus = HEADER_NAME_START;

			case	HEADER_NAME_START:
				ctx->Header.nameVal[ctx->Header.curNum].name = &p[i];
				ctx->Header.substatus = HEADER_NAME;

			case	HEADER_NAME:
				if(p[i] == COL)
				{
					ctx->Header.substatus = HEADER_VAL;
					p[i] = 0;
					chkpt = &p[i+1];
					ctx->Header.nameVal[ctx->Header.curNum].name = 
						strdup(ctx->Header.nameVal[ctx->Header.curNum].name);
					ctx->Header.substatus = HEADER_VAL_START;
				}
				break;

			case	HEADER_VAL_START:
				ctx->Header.nameVal[ctx->Header.curNum].value = &p[i];
				ctx->Header.substatus = HEADER_VAL;

			case	HEADER_VAL:
				if(p[i]==CR && p[i+1]==LF)
				{
					ctx->Header.substatus = HEADER_VAL_DONE;
					p[i] = p[i+1] = 0;
					chkpt = &p[i+1];
					i++;
					ctx->Header.nameVal[ctx->Header.curNum].value =
						strdup(ctx->Header.nameVal[ctx->Header.curNum].value);
				}
				break;


			case	HEADER_VAL_DONE:
				/* We come here if we have encountered CRLF after a
				 * header value. So, now it should be end of header or a
				 * new header starts.
				 */
				if(p[i] == CR)
				{
					ctx->Header.substatus = HEADER_VAL_DONE_CR;
				}
				else
				{
					ctx->Header.curNum++;
					ctx->Header.nameVal[ctx->Header.curNum].name = &p[i];
					ctx->Header.substatus = HEADER_NAME;
				}
				break;


			case	HEADER_VAL_DONE_CR:
				if(p[i] != LF)
					goto header_err;
				ctx->Header.substatus = HEADER_DONE_CRLF;
				break;

			case	HEADER_DONE_CRLF:
				if(p[i] != LF)
					goto header_err;
				ctx->rState = resp_body;
				break;
		}
	}
	
	if((ctx->Header.substatus != HEADER_DONE_CRLF) && chkpt )
	{
		strncpy(p,chkpt,len - (chkpt - p));
		ctx->lastOff = len - (chkpt - p);
	}

header_err:
	
	return ctx->Status.substatus;
}


int		ReadBody(HTTP_CTX	*ctx, int len)
{
	int		ret;
	char	*ptr;

	if(len == 0)
	{
		len = ctx->maxBodySize;
		ctx->bodyLen = 0;
	}
	else if (len <= ctx->lastOff)
	{
		ctx->bodyLen = len;
		ctx->rState = resp_done;
		return len;
	}

	ptr = ctx->readBuf[0].ptr;
	ctx->readBuf[0].ptr = malloc(len);	
	bcopy(ptr,ctx->readBuf[0].ptr,ctx->lastOff);
	len -= ctx->lastOff;

	free(ptr);
	ptr = NULL;
 
	do
	{
		ret	= recv(ctx->sockfd,ctx->readBuf[0].ptr+ctx->lastOff,
							len, MSG_DONTWAIT);

		if(ret <= 0  &&  errno != EAGAIN);
			break;
		if(ret == -1  &&  errno == EAGAIN);
			continue;
		
		len -= ret;
		ctx->bodyLen += ret;
		ctx->lastOff += ret;

		if(len == 0)
			break;

		//ParseBody(ctx);
		//if(ctx->rState != resp_body)
		//	break;

		//if(ctx->lastOff > (ctx->maxBodySize * 0.8))
		//{
		//	ptr = malloc(2 * ctx->maxBodySize);
		//	bcopy(ctx->readBuf[1].ptr,ptr,ctx->lastOff);
		//	free(ctx->readBuf[1].ptr);
		//	ctx->readBuf[1].ptr = ptr;
		//	ctx->maxBodySize = 2 * ctx->maxBodySize;
		//}

	} while (ret == -1 &&  errno == EAGAIN && ctx->lastOff < ctx->maxBodySize);

	if(len)
		ctx->rState = resp_err;
	else
		ctx->rState = resp_done;

	return ctx->rState;
}


char	*getRespBody(HTTP_CTX *ctx)
{
	return ctx->readBuf[0].ptr;
}

char	*getHeaderVal(HTTP_CTX *ctx,char *header)
{
	int		i;

	for(i=0; i<ctx->Header.curNum; i++)
	{
		if(strcmp(ctx->Header.nameVal[i].name,header)==0)
			return ctx->Header.nameVal[i].value;
	}
	return NULL;
}


cJSON	*ReadResponse(HTTP_CTX *ctx)
{
		int		status = 0;
		int		err	= 0;
		int		len	= 0,i;
		char	*lenstr, *body;
		cJSON	*jsn = NULL;

		ctx->rState = resp_init;
		ctx->lastOff = 0;
		bzero(&ctx->Status,sizeof(ctx->Status));
		for(i=0; i<ctx->Header.curNum;i++)
		{
			free(ctx->Header.nameVal[i].name);
			free(ctx->Header.nameVal[i].value);
			ctx->Header.nameVal[i].name = NULL;
			ctx->Header.nameVal[i].value = NULL;
		}
		ctx->Header.curNum = 0;
		ctx->Header.substatus = HEADER_START;

		ctx->rState = resp_status;
		while(ctx->rState == resp_status)
		{
			ReadStatus(ctx);
		}
		status = atoi(ctx->Status.status);
		if(status != STATUSCREATED)
		{
			err = status;
			goto	err;
		}

		while(ctx->rState == resp_header)
		{
			ReadHeader(ctx);
		}

		if(ctx->rState == resp_body)
		{
			lenstr = getHeaderVal(ctx,CONTENTLEN);
			if(lenstr)
				len = atoi(lenstr);
			else
				len = 0;

			ReadBody(ctx,len);

			if(ctx->rState == resp_done)
			{
				body = getRespBody(ctx);
				jsn = cJSON_Parse(body);
			}
		}

err:
	return jsn;
}


#ifdef	SELFTEST
main(int argc, char **argv)
{
	char		out[1024];
	int			i,len;
	int			testcase = atoi(argv[1]);
	HTTP_CTX	*ctx;

	testcase = 3;

	if(testcase == 1)
	{
		ctx = Login("nsroot","nsroot","10.102.28.133");
		AddVserver(ctx,"vsrvr_1","10.102.28.134",443,"SSL");
	}
	else if(testcase == 2)
	{
		DataPusher();
	}
	else if(testcase == 3)
	{
		HTTP_CTX	ctx;
		cJSON		*json,*cJc;
		char		*str;
		int			len;
		char		buf[64];

		ctx.rState = resp_init;
		allocReadBuf(&ctx);
		ctx.maxBodySize = 16 * 1024;
		ctx.sockfd = MakeSocket("127.0.0.1",atoi(argv[1]));

		if(ctx.sockfd <= 0)
		{
			printf("MakeSocket(\"127.0.0.1\",8081) : Failed\n");
			fflush(stdout);
			return 0;
		}

		json = javaLogin("nsroot","nsroot");
		jsonSendRecv(json,ctx.sockfd);

		json = javaAddServer("test_server_1","192.168.10.1");
		jsonSendRecv(json,ctx.sockfd);



		return;

		ctx.rState = resp_status;
		while(ctx.rState == resp_status)
		{
			ReadStatus(&ctx);
		}
		while(ctx.rState == resp_header)
		{
			ReadHeader(&ctx);
		}
		printf("Headers:\n");
		for(i=0; i<ctx.Header.curNum; i++)
		{
			printf("%s:%s\n",
				ctx.Header.nameVal[i].name,ctx.Header.nameVal[i].value);
		}

		if(ctx.rState == resp_body)
		{
			char	*len = getHeaderVal(&ctx,CONTENTLEN);
			if(len)
				i = atoi(len);
			else
				i = 0;

			ReadBody(&ctx,i);
			if(ctx.rState == resp_done)
			{
				cJSON	*jsn;
				len = getRespBody(&ctx);
				jsn = cJSON_Parse(len);
			}
		}
	}
}


int		DataPusher()
{
	int		sd,asd,datalen,len,optval=0;
	char	*data = TESTSTR;
	struct	sockaddr_in	addr;

	sd = socket(PF_INET,SOCK_STREAM,6);
	addr.sin_family 		=   PF_INET;
	addr.sin_port			=	htons(8081);
	addr.sin_addr.s_addr	=	INADDR_ANY;
	addr.sin_len			=	sizeof(addr);
	optval 					= 1;
	setsockopt(sd, SOL_SOCKET, SO_REUSEPORT, &optval, sizeof(optval));
	while(bind(sd,(struct sockaddr *)&addr,sizeof(addr)) )
	{
		printf("Retrying ... DataPush server failed to bind.\n");
		sleep(2);
	}
	listen(sd,5);
	asd = accept(sd,NULL,NULL);
	datalen = strlen(data);	
	while(datalen)
	{
		len = send(asd,data,datalen,0);
		printf("sent %d bytes left %d bytes\n",len,datalen-len);
		if(len <= 0)
			break;
		datalen -= len;
		data += len;
	}
}


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

#endif
