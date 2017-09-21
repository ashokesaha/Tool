#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <signal.h>
#include <errno.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <openssl/ossl_typ.h>
#include <openssl/bio.h>
#include <openssl/ssl.h>
#include <openssl/dh.h>
#include <openssl/ec.h>
#include <openssl/bio.h>
#include <sys/select.h>
#include "cJSON.h"


typedef struct _child_stat_ {
	int 						pid;
	int							pass;
	int							fail;
	struct 		_child_stat_	*next;	
} CHILD_STAT_t;


static int		doChild(int sd);
static int 		initSocket(int port);
static int  	WaitForChild(int kill);
static int	 	CleanChild();
static int		HandleArgs(char * buf);
static int		ProcessChildStat(CHILD_STAT_t *stat, int status);
static int	 	readCmdData(int , unsigned char * , int *);
static int		WriteResponse(char *, ...);


#define		MAXCHILD	4
#define		printf		WriteResponse

int			PORT = 0;
char		*CURDIR = NULL;
CHILD_STAT_t	*childStatFreeQ, *childStatActiveQ, *curChildStat;

int main(int argc, char **argv)
{
	int						asd, sd;
	int						len, childCount=0;
	int						i,pid = -1;
	int						status = 0, ret;
	char					namebuf[256];
	char					buf[1024];
	CHILD_STAT_t			*tChildStat;
	struct	sockaddr_in		from;
	fd_set					readfds;
	struct	timeval			tv;


	chdir("/tmp");

	len =  sizeof(buf) - 1;
#if 0
	ret = readCmdData(0, buf, &len);
	if(ret <= 0)
		return 0;

	if(strcmp(buf,"twinkletwinkle"))
		return 0;
	WriteResponse("%s","ocspresponder");

	len =  sizeof(buf) - 1;
	ret = readCmdData(0, buf, &len);
	if(ret <= 0)
		return ret;
	HandleArgs(buf);
#endif
	PORT = 4646;

	if(CURDIR)
		chdir(CURDIR);

	asd = initSocket(PORT);
	listen(asd,5);


	for(ret=0; ret < MAXCHILD * 2; ret++)
	{
		tChildStat = (CHILD_STAT_t *)malloc(sizeof(CHILD_STAT_t));
		tChildStat->pid = 0;
		tChildStat->next = childStatFreeQ;
		childStatFreeQ = tChildStat;
	}


	tv.tv_sec = 0;
	tv.tv_usec = 500 * 1024;
	while(1)
	{
		FD_ZERO(&readfds);
		FD_SET(0,&readfds);
		FD_SET(asd,&readfds);

		select(asd+1,&readfds,NULL,NULL,&tv);

		childCount -= CleanChild();

		if(FD_ISSET(0,&readfds))
		{
			len =  sizeof(buf) - 1;
			ret = readCmdData(0, buf, &len);
			if((ret <= 0) || (len == 0))
			{
				WriteResponse("Parent:: exiting after cleaning child.\n");
				WaitForChild(1);
				return 0;
			}

			HandleArgs(buf);
		}

		if(!FD_ISSET(asd,&readfds))
			continue;

		len = sizeof(from);
		childCount = 0;

		while(!childStatFreeQ)
		{
			WriteResponse("Waiting for childStatFreeQ");
			sleep(1);
			childCount -= CleanChild();
		}

		curChildStat		= childStatFreeQ;
		childStatFreeQ		= childStatFreeQ->next;
		curChildStat->next	= childStatActiveQ;
		childStatActiveQ	= curChildStat;
		curChildStat->pass  = curChildStat->fail = curChildStat->pid = 0;

		listen(asd,5);
		sd = accept(asd,(struct sockaddr *)&from,(void *)&len);
		if(sd <= 0)
		{
			perror("accept::");
			exit(0);
		}

		pid = fork();
		if(pid > 0)
		{
			curChildStat->pid = pid;
			childCount++;

		}
		else if (pid == 0)
		{ 
			ret = doChild(sd);
			close(sd);
			exit(ret);
		}
		childCount -= CleanChild();
	}
}




int	doChild(int sd)
{
	char	buf[8 * 1024];
	char	*ptr;
	int		ret = 0;

	ret = recv(sd,buf,sizeof(buf),0);
	printf("Received %d bytes\n", ret);

	ptr = strstr(buf,"\r\n\r\n");
	if(ptr)
		*ptr = 0;
	printf("[%s]\n", buf);
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
		WriteResponse("bind:: %s\n",errstr);
		perror("bind::");
		s = -1;
	}

	return s;
}


int	ProcessChildStat(CHILD_STAT_t *stat, int status)
{

	return 0;
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


int     CloseResponse()
{
	int             len = 0;
	fwrite((unsigned char *)&len,sizeof(len),1,stdout);
	fflush(stdout);
	return len;
}



static int	HandleArgs(char * buf)
{
	int	ret;
	cJSON	*cJ, *cJc;
	int		i;

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
		cJc = cJc->next;
	}
	return 0;
}



int  WaitForChild(int killl)
{
	CHILD_STAT_t	*p, **pp;
	int				pid,status = 0;

	if(killl)
	{
		for(p=childStatActiveQ; p; p = p->next)
			kill(p->pid,9);
	}

	while(childStatActiveQ)
	{
		pid=wait4(-1,&status,0,NULL);
		if(pid <= 0)
			break;
		for(pp=&childStatActiveQ; p=*pp; pp = &p->next)
		{
			if(p->pid == pid)	
			{
				ProcessChildStat(p,status);
				*pp = p->next;
			}
		}
	}
	return 0;
}


int	 CleanChild()
{
	int				count = 0;
	int				status, pid;
	CHILD_STAT_t	**pp, *p;

	while( (pid=wait4(-1,&status,WNOHANG,NULL)) > 0 )
	{
		for(pp=&childStatActiveQ; p=*pp; pp = &p->next)
		{
			if(p->pid == pid)	
			{
				ProcessChildStat(p,status);
				*pp = p->next;
				p->next = childStatFreeQ;
				childStatFreeQ = p;
				count++;
			}
		}
	}
	return count;
}
