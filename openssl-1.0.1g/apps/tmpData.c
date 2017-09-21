#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <errno.h>
#include <sys/select.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <sys/select.h>


int		RESPSIZE = 0;
int		PKTSIZE  = 0;
int		WRITESIZE  = 0;
int		PKTDELAY = 0;
int		PUSHPOS  = 0;
int		PORT  = 0;

int		DELAY1(int unit);
int		DELAY2(int unit);
int 	initSocket(int port);
int		doResponse(int asd);
int		readRequest(int sd, char *buf);

extern	char RESPDATA[];
extern  int  GetRespDataSize();


#if 0
#define SERVERRESP  "HTTP1/1 200 OK\r\n\
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
#endif


#define SERVERRESP  "HTTP/1.1 200 OK\r\n\
Content-Type: text/html\r\n\
Connection: keep-alive\r\n\
Content-Length: %d\r\n\
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

	hdrlen = sprintf(headerBuf,SERVERRESP,totRespSize);

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

	sd = initSocket(PORT);
	listen(sd,5);

	while(1)
	{
		FD_ZERO(&readfds);
		FD_SET(sd,&readfds);
		printf("waiting on select 1..\n");
		select(sd+1,&readfds,NULL,NULL,0);
		printf("out of select 1..\n");
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
				FD_ZERO(&readfds);
				FD_SET(asd,&readfds);

				tv.tv_sec = 2;
				tv.tv_usec = 0;

				if(select(asd+1,&readfds,NULL,NULL,&tv) <= 0)
					break;

				bzero(buf,sizeof(buf));
				ret = readRequest(asd,buf);
				if(ret > 0)
					doResponse(asd);
				else
					break;
			}
			close(asd);
			asd = 0;
		}
	}
}


int	doResponse(int asd)
{
	int		totRespSize = GetRespDataSize();
	int		hdrlen,len,ret,val;
	char	headerBuf [1024];
	char	buf[1024];
	char	*resp = RESPDATA;
	struct	timeval tv;
	char	outData[9 * 1024];


	tv.tv_sec = 0;
	tv.tv_usec = 500000;
	ret = setsockopt(asd,SOL_SOCKET,SO_RCVTIMEO,&tv,sizeof(tv));
	if(ret < 0)
		perror("setsockopt::");
	

	hdrlen = sprintf(headerBuf,SERVERRESP,RESPSIZE);
	
	bcopy(headerBuf,outData,hdrlen);
	bcopy(resp,&outData[hdrlen],RESPSIZE);


	len = 0;
	ret = 0;
	resp = outData;
	while (len < RESPSIZE+hdrlen)
	{
		ret = write(asd,resp,RESPSIZE+hdrlen-len); 
		if(ret <= 0)
			break;
		len += ret;
		resp += ret;
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


int		DELAY2(int unit)
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
		if((ret == -1) && (errno == EAGAIN))
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
	printf("read [%s]\n",buf);	
	return len;
}
