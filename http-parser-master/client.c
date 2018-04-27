#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <signal.h>
#include <errno.h>
#include <sys/resource.h>


int     initSocket(char *ip, int port);
int		smallSend(int s, char *buf);


main(int argc, char **argv)
{
	char	*ip = argv[1];
	int		port = atoi(argv[2]);
	int		s, ret;
	char	*POST = "POST /somepage.php HTTP/1.1\r\nHost: example.com\r\nContent-Length: 19\r\n\r\nname=ruturajv&sex=m" ;

	s = initSocket(ip,port);
	if(s < 0)
		return;

	//ret = send(s,POST,strlen(POST),0);
	ret = smallSend(s,POST);
	printf("send : sent %d bytes\n", ret);

}


int	smallSend(int s, char *buf)
{
	int	chunks[] = {1,2,3,4,5,6,7,8,9};
	int	numchunks = sizeof(chunks)/sizeof(chunks[0]);
	int	i,sz,ret;
	int rem = strlen(buf);
	char *p = buf;

	while(rem > 0)
	{
		for(i=0; (i<numchunks) && (rem > 0); i++)
		{
			if(rem < chunks[i])
				sz = rem;
			else
				sz = chunks[i];

			rem -= sz;
			ret = send(s,p,sz,0);
			p += sz;
		}
		i = 0;
	}
	return 0;
}



int 	initSocket(char *ip, int port)
{
	int	s = -1, val, ret=0;
	struct sockaddr_in server;
	struct	timeval	tv;

	s = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);

	memset((char *)&server,0,sizeof(server));
	server.sin_family=AF_INET;
	server.sin_port=htons((unsigned short)port);
	server.sin_addr.s_addr = inet_addr(ip);	

	val = 1;
	setsockopt(s,SOL_SOCKET,SO_REUSEADDR,&val,sizeof(val));

	ret = connect(s,(struct sockaddr *)&server, sizeof(server));
	if(ret)
	{
		printf("connect failed:\n");
		return -1;
	}

	return s;
}
