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


typedef	struct _resp_profile_ {
	int	numEntries; //number of <8 digit number> entries
	int	recSize;	//How many bytes of plain text is made a record
	int	recBufNum;
} RESP_PROFILE;


int		glb_count = 0;

int	BindSocket(int port)
{
	int		ret;
	int		sd;
	struct	sockaddr_in	addr;

	sd = socket(PF_INET,SOCK_STREAM,6);

	bzero(&addr,sizeof(addr));
	addr.sin_family	=	PF_INET;
	addr.sin_port	=	htons(port);
	addr.sin_addr.s_addr =  INADDR_ANY;
	addr.sin_len	= sizeof(addr);

	ret = bind(sd,(struct sockaddr *)&addr,sizeof(addr));
	if(ret)
		return ret;
	listen(sd,10);
	return sd;
}


int	SelectAndWait(fd_set r, fd_set w, fd_set e)
{
	struct	timeval tv;

	tv.tv_sec	= 1;
	tv.tv_usec	= 0;

	while(1)
	{


	}
}


int		DoChild(int sfd)
{
	char	buf[64];
	int		len,i;
	int		ret,wret;
	
printf("[%d] count is %d\n",getpid(),glb_count);
	sprintf(buf,"count is %d\n",glb_count);
	len = strlen(buf);
	i = 0;
	while (i < len)
	{
		ret = send(sfd,&buf[i],len-i,0);
		if(ret <= 0)
			break;
		i += ret;
	}
	close(sfd);
	return i;
}


main(int argc, char **argv)
{
	int		pid[4];
	int		i,wret;
	int		sockfd,sfd;
	int		status;
	char	buf[64];

	fd_set			rfd;
	struct	timeval tv;

	sockfd = BindSocket(atoi(argv[1]));
	if(sockfd <= 0)
		exit(0);

	FD_ZERO(&rfd);
	FD_SET(sockfd,&rfd);

	tv.tv_sec	= 1;
	tv.tv_usec	= 0;


	while((wret = select(sockfd+1,&rfd,NULL,NULL,&tv)) >= 0)
	{
		waitpid(-1,&status,WNOHANG);

		if(wret == 0)
		{
			FD_SET(sockfd,&rfd);
			continue;
		}

		if(FD_ISSET(sockfd,&rfd))
		{
			sfd = accept(sockfd,NULL,NULL);
			wret = recv(sfd,buf,1,MSG_PEEK);
			if(wret > 0)
			{
				glb_count++;
				wret = fork();
				if(wret == 0)
				{
					DoChild(sfd);
					return;
				}
			}
			close(sfd);
		}
		FD_SET(sockfd,&rfd);
	}
}
