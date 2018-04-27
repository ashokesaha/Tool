#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include "common_utils.h"


typedef struct _child_stat_ {
	int							id;
	int 						pid;
	int							pass;
	int							fail;
	struct 		_child_stat_	*next;	
} CHILD_STAT_t;


char	*CHDIR   = NULL;
char	*LOGFILE = NULL;
char	*FIRSTRESPONSE = NULL;
FILE	*childLogFP   = NULL;
FILE	*parentLogFP   = NULL;
int		(*ArgHandlerP)(char *) = NULL;
int		(*TestHandlerP)()= NULL;
int		CHILDCOUNT = 1;
int		TOUTMSEC = 1000;
int		CHILDID = 1;

CHILD_STAT_t			*childStatQ = NULL;


static int	CleanChild();
static int  WaitForChild(int);
static int	SetChildLogFile();



int SetTestHandler(int(*f)(int))
{
	TestHandlerP = f;
	return 0;
}


int SetChildCount(int count)
{
	CHILDCOUNT = count;
	return 0;
}


int	SetArgHandler(int(*f)(char *))
{
	ArgHandlerP = f;
	return 0;
}


int	SetFirstResp(char *resp)
{
	FIRSTRESPONSE = strdup(resp);
	return 0;
}


int	SetCHDIR(char *dir)
{
	CHDIR = strdup(dir);
	chdir(CHDIR);
	return 0;
}


int	SetLogFile(char *filename)
{
	char	fname[64];
	sprintf(fname,"/tmp/%s.%d",filename,getpid());
	LOGFILE = strdup(fname);
	parentLogFP = fopen(LOGFILE,"w");
	setbuf(parentLogFP,NULL);
	return 0;
}



int 	ServerSocket(char *ip, int port)
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





int	ClientSocket(char *ip,int port)
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

	if(TOUTMSEC >= 1000)
	{
		tV.tv_sec	= TOUTMSEC/1000;
	}
	tV.tv_usec	= (TOUTMSEC % 1000) * 1000;

	setsockopt(sd,SOL_SOCKET,SO_RCVTIMEO,&tV,sizeof(tV));

	ret = connect(sd,(struct sockaddr *)&addr,sizeof(addr));

	alarm(0);
	if(ret < 0)
		return -1;
	return sd;
}


int	WriteResponse(char *format, ...)
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




int	 readCmdData(int fd, unsigned char * buf, int *len)
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
		*len = 0;
	return *len;
}



int ServerRun(int asd)
{
	char					buf[1024];
	int						len,ret,pid;
	struct	timeval			tv;
	fd_set					readfds;
	CHILD_STAT_t			*tChildStat;

	len =  sizeof(buf) - 1;
	ret = readCmdData(0, buf, &len);
	if(ret <= 0)
	{
		char *m = "Failed to read first data\n";
		fwrite(m,strlen(m),1,parentLogFP);
		fclose(parentLogFP);
		return 0;
	}

	if(strcmp(buf,"twinkletwinkle"))
	{
		char *m = "Invalid client init string\n";
		fwrite(m,strlen(m),1,parentLogFP);
		fclose(parentLogFP);
		return 0;
	}
	WriteResponse("%s",FIRSTRESPONSE);

	tv.tv_sec = 0;
	tv.tv_usec = 500 * 1024;
	while(1)
	{
		FD_ZERO(&readfds);
		FD_SET(0,&readfds);

		select(1,&readfds,NULL,NULL,&tv);
	

		if(FD_ISSET(0,&readfds))
		{
			fprintf(parentLogFP,"calling WaitForChild(1)\n");
			WaitForChild(1);
			fprintf(parentLogFP,"out of WaitForChild(1)\n");

			len =  sizeof(buf) - 1;
			ret = readCmdData(0, buf, &len);
			if(ret <= 0)
			{
				char *m = "failed to read command\n";
				fwrite(m,strlen(m),1,parentLogFP);
				fwrite(buf,strlen(buf),1,parentLogFP);
				fclose(parentLogFP);
				break;
			}
	
			ret = (*ArgHandlerP)(buf);
			if(ret < 0)
			{
				char *m = "command parse failure\n";
				fwrite(m,strlen(m),1,parentLogFP);
				fwrite(buf,strlen(buf),1,parentLogFP);
				continue;
			}

			//WaitForChild(1);
			pid = fork();

			if(pid > 0)
			{
				fprintf(parentLogFP,"Adding child with pid %d\n",pid);
				AddChild(pid);
			}
			else if (pid == 0)
			{
				SetChildLogFile();
				fprintf(childLogFP,"OOpened child log:\n");
				ret = (*TestHandlerP)();
				fprintf(childLogFP,"TestHandlerP returned:\n");
				exit(ret);
			}
			else
			{
				goto Exit;
			}
		}
	}

Exit:
	WaitForChild(1);
}



#if 0
int	AcceptLoop(int asd,int maxchild, int *keepRunning,int (*f)(int), int(*g)(int))
{
	fd_set			readfds;
	struct  timeval	tv;
	int				childCount = 0;
	
	tv.tv_sec = 0;
	tv.tv_usec = 500 * 1024;
 
	while(*keepRunning)
	{
		FD_ZERO(&readfds);
		FD_SET(asd, &readfds);
		FD_SET(0, &readfds);

		select(asd+1,&readfds,NULL,NULL,&tv);

		while(wait4(-1,&status,WNOHANG,NULL) > 0)
			childCount--;

		if(FD_ISSET(0,&readfds))
		{
			(*g)(0);
		}

		if(FD_ISSET(asd,&readfds))
		{
			listen(asd,5);
			sd = accept(asd,(struct sockaddr *)&from,(void *)&len);
			if(sd <= 0)
				break;

			if(childCount >= maxchild)
			{
				ret = wait4(-1,&status,0,NULL);
				if(ret > 0)
					childCount--;
			}
		
			pid = fork();
			if(pid > 0)
			{
				childCount++;
			}
			else if (pid == 0)
			{
				ret = (*f)(sd);
				exit(ret);
			}
			else 
			{
				;
			}
		}
	}

	while(childCount)
	{
		ret = wait4(-1,&status,0,NULL);
		if(ret > 0)
			childCount--;
	}

	return 0;
}
#endif


static int	SetChildLogFile()
{
	char	fname[64];
	sprintf(fname,"%s.%d",LOGFILE,getpid());
	//sprintf(fname,"/tmp/ocsp.child.%d",LOGFILE,getpid());
	LOGFILE = strdup(fname);
	childLogFP = fopen(LOGFILE,"w");
	setbuf(childLogFP,NULL);
fprintf(childLogFP,"opened logfile %s\n",LOGFILE);
	return 0;
}

static int  WaitForChild(int killl)
{
	CHILD_STAT_t	*p, **pp;
	int				pid,status = 0;

	if(killl)
	{
		for(p=childStatQ; p; p = p->next)
			kill(p->pid,9);
	}

	while(childStatQ)
	{
		pid=wait4(-1,&status,0,NULL);
		if(pid <= 0)
			break;
		for(pp=&childStatQ; p=*pp; pp = &p->next)
		{
			if(p->pid == pid)	
			{
				*pp = p->next;
			}
		}
	}
	return 0;
}


static int	 CleanChild()
{
	int				count = 0;
	int				status, pid;
	CHILD_STAT_t	**pp, *p;

	while( (pid=wait4(-1,&status,WNOHANG,NULL)) > 0 )
	{
		for(pp=&childStatQ; p=*pp; pp = &p->next)
		{
			if(p->pid == pid)	
			{
				*pp = p->next;
				p->next = childStatQ;
				childStatQ = p;
				count++;
			}
		}
	}
	return count;
}


int AddChild(int pid)
{
	CHILD_STAT_t	*tChildStat;
	tChildStat = (CHILD_STAT_t *)malloc(sizeof(CHILD_STAT_t));
	tChildStat->pid = pid;
	tChildStat->next = childStatQ;
	childStatQ = tChildStat;
	usleep(100 * 1000);
	return 0;
}
