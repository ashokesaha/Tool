#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/wait.h>

#include "openssl/x509.h"
#include "openssl/ssl.h"
#include "openssl/err.h"
#include "openssl/pem.h"
#include "openssl/rand.h"
#include "openssl/ocsp.h"
#include "openssl/bn.h"
#include "cJSON.h"
#include "nitro_lib.h"


//#define		REQUEST		"GET /ashwin_test.txt HTTP/1.1\r\nHost: %s\r\nConnection: keep-alive\r\n\r\n"
#define		REQUEST		"GET /index.html HTTP/1.1\r\nHost: %s\r\nConnection: keep-alive\r\n\r\n"
#define		REQLEN		strlen(REQUEST)

int	MakeSocket(char *ip,int port)
{
	int		ret;
	int		sd;
	struct	sockaddr_in	addr;
	struct	timeval	tV;


	sd = socket(PF_INET,SOCK_STREAM,6);
	bzero(&addr,sizeof(addr));
	addr.sin_family	=	PF_INET;
	addr.sin_port	=	htons(port);
	addr.sin_addr.s_addr =  inet_addr(ip);
	addr.sin_len	= sizeof(addr);

	bzero(&tV,sizeof(tV));
	tV.tv_sec	= 2;
	tV.tv_usec	= 1000;
	setsockopt(sd,SOL_SOCKET,SO_RCVTIMEO,&tV,sizeof(tV));

	ret = connect(sd,(struct sockaddr *)&addr,sizeof(addr));
	if(ret < 0)
		return -1;

	return sd;
}



main(int argc,char **argv)
{
	const SSL_METHOD    *v30Method = NULL;
	const SSL_METHOD    *v31Method = NULL;
	const SSL_METHOD    *v32Method = NULL;
	const SSL_METHOD    *v33Method = NULL;
	SSL_CTX				*CTX;
	BIO					*sbio;
	SSL					*con;
	int					sd,ecode,rlen;
	char				rBuf[8192];
	volatile int		Delay = 0x9FFFF;
	int					pipecount = 1;

	SSL_library_init();

    v30Method   = SSLv3_client_method();
    v31Method   = TLSv1_client_method();
    v32Method   = TLSv1_1_client_method();
    v33Method   = TLSv1_2_client_method();


	//CTX			= SSL_CTX_new(v30Method);
	CTX			= SSL_CTX_new(v33Method);
	if(!SSL_CTX_set_cipher_list(CTX,"AES"))
	{
		printf("Failed to set cipher ..\n");
		return 0;
	}

	if(argc >= 4)
		pipecount = atoi(argv[3]);

	if((sd = MakeSocket(argv[1], atoi(argv[2]))) < 0)
	{
		return 0;
	}

	Delay = atoi(argv[3]);

	con = SSL_new(CTX);
	sbio = BIO_new_socket(sd,BIO_NOCLOSE);
	SSL_set_bio(con,sbio,sbio);

	SSL_set_connect_state(con);
	SSL_set_no_empty_frag(con);
	ecode	= SSL_connect(con);
	if(ecode < 0)
	{
		printf("SSL_connect failed..\n");
		return 0;
	}

	rlen = sprintf(rBuf,REQUEST,argv[1]);


	while(pipecount)
	{
		ecode	= SSL_write(con,rBuf,rlen);
		if(ecode != rlen)
		{
			printf("Writing request 1 failed ecode %d\n",ecode);
			return 0;
		}
		pipecount--;
		//while(Delay--);
	}

	
	while(1)
	{
		ecode = SSL_read(con,rBuf,8090);
		if(ecode <= 0)
		{
			break;	
		}
		printf("%s",rBuf);
		bzero(rBuf,sizeof(rBuf));
	}
	printf("\n");
	//sleep(2);
}
