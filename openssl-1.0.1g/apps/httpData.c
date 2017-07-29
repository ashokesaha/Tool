#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <getopt.h>
#include <errno.h>
#include <sys/select.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <sys/select.h>
#include "cJSON.h"


int		RESPSIZE = 0;
int		PKTSIZE  = 0;
int		WRITESIZE  = 0;
int		PKTDELAY = 0;
int		PUSHPOS  = 0;
int		PORT  = 0;

int				DELAY1(int unit);
volatile int	DELAY2(int unit);
int 			initSocket(int port);
int				doResponse(int asd);
int				readRequest(int sd, char *buf);
static int		HandleArgs(char * buf);
static int		WriteResponse(char *format, ...);
static int		readCmdData(int fd, unsigned char * buf, int *len);

extern	char RESPDATA[];
extern  int  GetRespDataSize();


#define SERVERRESP  "HTTP/1.1 200 OK\r\n\
Content-Type: text/html; charset=ISO-8859-4\r\n\
Content-Length: %d\r\n\
HEADERONE: HEADERONE\r\n\
HEADERTWO: HEADERTWO\r\n\
HEADERTHREE: HEADERTHREE\r\n\
HEADERFOUR: HEADERFOUR\r\n\
HEADERFIVE: HEADERFIVE\r\n\
HEADERSIX: HEADERSIX\r\n\
HEADERSEVEN: HEADERSEVEN\r\n\
HEADEREIGHT: HEADEREIGHT\r\n\
HEADERNINE: HEADERNINE\r\n\
HEADERTEN: HEADERTEN\r\n\
HEADERELEVEN: HEADERELEVEN\r\n\
HEADERTWELVE: HEADERTWELVE\r\n\
HEADERTHIRTEEN: HEADERTHIRTEEN\r\n\
\r\n"


main(int argc, char **argv)
{
	char	ch;
	int		totRespSize = GetRespDataSize();
	int		hdrlen,len,ret;
	char	headerBuf [1024];
	int		debug = 1;
	int		sd,asd;
	fd_set	readfds;
	fd_set	readfds2;
	struct  timeval	tv;
	char	buf[1024];

	struct option longopts[] = {
		{"port",		required_argument,  		NULL,'p'},
		{"respsize",	required_argument,  		NULL,'a'},
		{"pktsize",		optional_argument, 			NULL,'b'},
		{"pktdelay",	optional_argument,			NULL,'c'},
		{"pushpos",		optional_argument,			NULL,'d'},
		{"writesize",	optional_argument, 			NULL,'e'},
		{0,0,0,0}
	};

	//while(debug);

	chdir("/mnt/ToolPkg/Server");
	len =  sizeof(buf) - 1;
	ret = readCmdData(0, buf, &len);
	if(ret <= 0)
		return 0;

	if(strcmp(buf,"twinkletwinkle"))
		return 0;
	WriteResponse("%s","whatyouare");

	len =  sizeof(buf) - 1;
	ret = readCmdData(0, buf, &len);
	if(ret <= 0)
		return ret;
	HandleArgs(buf);


	hdrlen = sprintf(headerBuf,SERVERRESP,totRespSize);


#if 0
	while ((ch = getopt_long(argc, argv, "a:b:c:d:",longopts,NULL)) != -1)
	{
		switch(ch)
		{
			case 'a': RESPSIZE = atoi(optarg); break;
			case 'b': PKTSIZE  = atoi(optarg); break;
			case 'c': PKTDELAY = atoi(optarg); break;
			case 'd': PUSHPOS  = atoi(optarg); break;
			case 'e': WRITESIZE  = atoi(optarg); break;
			case 'p': PORT  = atoi(optarg); break;
		}
	}
#endif


	srandomdev();

	sd = initSocket(PORT);
	listen(sd,5);

	while(1)
	{
		FD_ZERO(&readfds);
		FD_SET(sd,&readfds);

		select(sd+1,&readfds,NULL,NULL,0);

		if(FD_ISSET(sd,&readfds))
		{
			asd = accept(sd,NULL,NULL);
			if(asd < 0)
			{
				printf("accept failed..\n");
				exit(0);
			}
			while(1)
			{
				FD_ZERO(&readfds2);
				FD_SET(asd,&readfds2);

				tv.tv_sec = 2;
				tv.tv_usec = 0;
				if(select(asd+1,&readfds2,NULL,NULL,&tv) <= 0)
				{
					perror("select 2:");
					break;
				}

				if(FD_ISSET(asd,&readfds2))
				{
					bzero(buf,sizeof(buf));
					ret = readRequest(asd,buf);
					if(ret > 0)
						doResponse(asd);
					else if(ret <= 0)
						break;
				}
			}
			close(asd);
			asd = 0;
		}
	}
}


int	doResponse(int asd)
{
	int		totRespSize = RESPSIZE;
	int		hdrlen,len,ret,val;
	char	headerBuf [1024];
	char	buf[1024];
	char	*resp = RESPDATA;
	struct	timeval tv;
	char	outData[9 * 1024];
	int		writesize,pktsize;
	long	R = random();


	//if(PUSHPOS)
	if(R & 0x00008000)
	{
		val = 1;
		ret = setsockopt(asd,IPPROTO_TCP,TCP_NODELAY,&val,sizeof(val));
		if(ret < 0)
			perror("setsockopt TCP_NODELAY");
	}
	else
	{
		val = 1;
		ret = setsockopt(asd,IPPROTO_TCP,TCP_NOPUSH,&val,sizeof(val));
		if(ret < 0)
			perror("setsockopt TCP_NOPUSH");
	}

#if 0
	val = R & 0x0FFF0000;
	ret = setsockopt(asd,IPPROTO_TCP,TCP_MAXSEG,&val,sizeof(val));
	if(ret < 0)
		perror("setsockopt TCP_MAXSEG");
	else
		printf("setsockopt: TCP_MAXSEG sucessfully set %d\n",val);
#endif


	tv.tv_sec = 1;
	tv.tv_usec = 0;
	ret = setsockopt(asd,SOL_SOCKET,SO_RCVTIMEO,&tv,sizeof(tv));
	if(ret < 0)
		perror("setsockopt SO_RCVTIMEO");
	

	totRespSize = (R & 0x01FFF000) >> 12;
	resp = malloc(totRespSize+1);
	bcopy(RESPDATA,resp,totRespSize);
	if(totRespSize >= 4)
		bcopy("A55A",&resp[totRespSize-4],4);
	else if(totRespSize >= 3)
		bcopy("55A",&resp[totRespSize-3],3);
	else if(totRespSize >= 2)
		bcopy("5A",&resp[totRespSize-2],2);
	else if(totRespSize >= 1)
		bcopy("A",&resp[totRespSize-1],1);

	hdrlen = sprintf(headerBuf,SERVERRESP,totRespSize);
	
	len = 0;
	while(len < hdrlen)
	{
		ret = send(asd,&headerBuf[len],hdrlen - len,0); 
		if(ret <= 0)
			break;
		len += ret;
	}

	len = 0;
	ret = 0;
	//while (len < RESPSIZE)
	while (len < totRespSize)
	{
		//writesize = WRITESIZE;
		//pktsize = PKTSIZE;

		R = random();
		writesize = (R & 0x00FFF000) >> 12;

		if ((totRespSize - len) < writesize)
			writesize = totRespSize - len;

		//if(writesize < pktsize)
		//	pktsize = writesize;

		ret = write(asd,resp,writesize); 
		if(ret <= 0)
			break;

		resp += ret;
		len += ret;
		//DELAY2(PKTDELAY);
		DELAY2((R & 0x1FF80000) >> 19);
	}

	return 0;
}


int		DELAY1(int unit)
{
	int		i;
	volatile int val = 0xFF;
	for(i=0; i<unit; i++)
	{
		val = 0xFF;
		while(val--);
	}
	return 0;
}


volatile int		DELAY2(int unit)
{
	int		i;
	volatile int val = (0xFFFF * unit);
	while(val--);
	return 0;
}


int 	initSocket(int port)
{
	int	s = -1, val;
	struct sockaddr_in server;

	s = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
	memset((char *)&server,0,sizeof(server));
	server.sin_family=AF_INET;
	server.sin_port=htons((unsigned short)port);
	server.sin_addr.s_addr = INADDR_ANY;	

	val = 1;
	setsockopt(s,SOL_SOCKET,SO_REUSEADDR,&val,sizeof(val));

	if (bind(s,(struct sockaddr *)&server,sizeof(server)) == -1)
	{
		char	*errstr = strerror(errno);
		perror("bind::");
		s = -1;
	}

	return s;
}


int	readRequest(int sd, char *buf)
{
	char	*ptr = buf;
	int		len,ret;

	
	len = 0;

	while(1)
	{
		ret = recv(sd,&buf[len],1024,0);
		if((ret <= 0) && (errno == EAGAIN))
			continue;
		else if (ret <= 0)
			break;
		else 
		{
			len += ret;
			if((len >= 4) && (bcmp(&buf[len-4],"\r\n\r\n",4)==0))
				break;
		}
	}
	return ret;
}


static int  HandleArgs(char * buf)
{
	int ret;
	cJSON   *cJ, *cJc;
	int     i;

    if(buf[0] == '[')
        bcopy(buf+1,buf,strlen(buf)-1);
	
	cJ  = cJSON_Parse(buf);
	if(!cJ)
	{
		WriteResponse("cJSON_Parse failed\n");
		fflush(stderr);
		exit(0);
	}

	cJc = cJ->child;
	while(cJc)
	{
		if(strcmp(cJc->string,"listen_port") == 0)
		{
			PORT = atoi(cJc->valuestring);
		}
	}

	return 0;
}


static int	WriteResponse(char *format, ...)
{
	char	buf[1024];
	char	tbuf[1024];
	int		len;
	va_list valist;
	
	buf[0] = 0;
	va_start(valist, format);
	vsnprintf(tbuf,sizeof(tbuf) - strlen(buf) - 1, format,valist);
	strcat(buf,tbuf);
	len = strlen(buf);

	va_end(valist);
	fwrite((unsigned char *)&len,sizeof(len),1,stdout);
	fwrite((unsigned char *)buf,len,1,stdout);
	fflush(stdout);
	return len;
}



static int	 readCmdData(int fd, unsigned char * buf, int *len)
{
	int	ret,rlen;
	unsigned char *p = buf;

	ret = recv(fd,buf,4,0);
	if(ret <= 0)
		return 0;
	
	rlen = *(int *)buf;	
	rlen = ntohl(rlen);
	if(*len < rlen)
		return 0;
	
	*len = rlen;
	while(rlen > 0)
	{
		ret = recv(fd,p,rlen,0);
		if(ret <= 0)
			break;
		p += ret;
		rlen -= ret;
	}
	
	if(rlen)
		*len = 0; //error
	return *len;
}
