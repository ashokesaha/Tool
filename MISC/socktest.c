#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define	GETS	"GET /\n\n"
#define	GETL	strlen(GETS)

main(int argc,char **argv)
{
	int		port  = atoi(argv[2]);
	int		rport = atoi(argv[3]);
	char	*ip  = argv[1];
	int		sd;
	char	buf[1024];
	struct	sockaddr_in	laddr,raddr;

	sd = socket(PF_INET,SOCK_STREAM,6);

	bzero(&laddr,sizeof(laddr));
	bzero(&raddr,sizeof(raddr));

	laddr.sin_len = sizeof(laddr);
	laddr.sin_family = AF_INET;
	laddr.sin_port = htons(port);
	laddr.sin_addr.s_addr = htonl(INADDR_ANY);

	bind(sd,(struct sockaddr *)&laddr,sizeof(laddr));

	raddr.sin_len = sizeof(laddr);
	raddr.sin_family = AF_INET;
	raddr.sin_port = htons(rport);
	raddr.sin_addr.s_addr = inet_addr(ip);

	connect(sd,(struct sockaddr *)&raddr,sizeof(raddr));

	send(sd,GETS,GETL,0);
	
	bzero(buf,sizeof(buf));
	recv(sd,buf,1000,0);

	printf("%s\n",buf);
}
