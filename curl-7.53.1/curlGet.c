#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <fcntl.h>
#include <string.h>
#include <strings.h>
#include <sys/stat.h>
#include "curl/curl.h"
#include <sys/types.h>
#include <sys/socket.h>
#include "cJSON.h"

typedef  enum {
	enNONE,
	enIP,
	enPORT,
	enCMD
} ARGVAL_t;


typedef	enum {
	mNONE,
	mGET,
	mPUT,
	mPOST
} Misc_t;



char	*gIP = NULL;
int		gPORT = 0;
int		gCMD = 0;


static size_t GET_callback(char *ptr, size_t size, size_t nmemb, void *userdata)
{
	printf("%s",ptr);
	return nmemb;
}


static size_t PUT_callback(char *ptr, size_t size, size_t nmemb, void *stream)
{
	char buf[] =	"0123456789012345678901234567890123456789\
					 0123456789012345678901234567890123456789\
					 0123456789012345678901234567890123456789" ;
					
	if(size >= 64)
		return 0;

	bcopy(&buf[size],ptr,8);
	return 8;
}



static int     ParamStrToCode(char *param)
{
	if(strcmp(param,"ip") == 0)	return enIP;
	else if(strcmp(param,"port") == 0) return enPORT;
	else if(strcmp(param,"cmd") == 0) return enCMD;
	else return enNONE;
}




static int	HandleArgs(char * buf)
{
	int	ret;
	cJSON	*cJ, *cJc;

	if(buf[0] == '[')
		bcopy(buf+1,buf,strlen(buf)-1);

	cJ  = cJSON_Parse(buf);
	if(!cJ)
	{
		printf("cJSON_Parse failed\n");
		fflush(stderr);
		exit(0);
	}

	cJc = cJ->child;
	while(cJc)
	{
		ret = ParamStrToCode(cJc->string);
		switch(ret)
		{
			case enIP :
			{
				gIP = strdup(cJc->valuestring);break;
			}

			case enPORT :
			{
				gPORT = cJc->valueint;break;
			}

			case enCMD :
			{
				char *p = cJc->valuestring;
				while(*p) {*p = toupper(*p); p++;}

				if(strcmp(cJc->valuestring,"GET") == 0)
					gCMD = mGET;
				else if(strcmp(cJc->valuestring,"PUT") == 0)
					gCMD = mPUT;
				else if(strcmp(cJc->valuestring,"POST") == 0)
					gCMD = mPOST;
			}
		}
		cJc = cJc->next;
	}
	return 0;
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
		*len = 0; //error
	return *len;
}



int	 writeStatusData(int fd, unsigned char * buf, int len)
{
	char	tbuf[8] = "";
	int wlen = 0, ret = 0;
	unsigned char *p;

	wlen = 4;
	p = (unsigned char *)&len;
	while(wlen)
	{
		ret = send(fd,p,wlen,0);
		if(ret <= 0)
			return 0;
		wlen -= ret;
		p += ret;
	}
	if(wlen)
		return 0;

	wlen = len;
	ret = 0;
	p = buf;
	while(wlen)
	{
		ret = send(fd,p,wlen,0);
		if(ret <= 0)
			return 0;
		wlen -= ret;
		p += ret;
	}
	if(wlen)
		return 0;
	
	return len;
}






main()
{
	int	ret,len;
	unsigned char buf[1024];
	volatile int debug = 1;

	GET_Action();
}


int GET_Action()
{
	CURL		*curl;
	CURL		*curl2;
	int			pid;
	CURLcode	res;
	char		url[1024];
	
	sprintf(url,"https://10.102.28.237:443/f.html");

	curl = curl_easy_init();
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, GET_callback);
	curl_easy_setopt(curl, CURLOPT_URL, url);
	curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0);
	curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0);

	curl2 = curl_easy_init();
	curl_easy_setopt(curl2, CURLOPT_WRITEFUNCTION, GET_callback);
	curl_easy_setopt(curl2, CURLOPT_URL, url);
	curl_easy_setopt(curl2, CURLOPT_SSL_VERIFYPEER, 0);
	curl_easy_setopt(curl2, CURLOPT_SSL_VERIFYHOST, 0);

	pid = fork();

	if(pid > 0)
	{
		res = curl_easy_perform(curl);
    	curl_easy_cleanup(curl);
	}
	else if (pid == 0)
	{
		res = curl_easy_perform(curl2);
    	curl_easy_cleanup(curl2);
	}

	return 0;
}



int PUT_Action()
{
	CURLM		*curlm;
	CURL		*curl, *curl2;
	CURLcode	res;
	char		url[1024];
	int		pid;

	//sprintf(url,"http://%s:%d/",gIP,(gPORT ? gPORT : 80));
	sprintf(url,"https://10.102.28.237:443/f.html");

	curlm = curl_multi_init();

	curl = curl_easy_init();
	curl_easy_setopt(curl, CURLOPT_READFUNCTION, PUT_callback);
	curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);
	curl_easy_setopt(curl, CURLOPT_PUT, 1L);
	curl_easy_setopt(curl, CURLOPT_URL, url);
	curl_easy_setopt(curl, CURLOPT_INFILESIZE_LARGE,64);

	curl2 = curl_easy_init();
	curl_easy_setopt(curl2, CURLOPT_READFUNCTION, PUT_callback);
	curl_easy_setopt(curl2, CURLOPT_UPLOAD, 1L);
	curl_easy_setopt(curl2, CURLOPT_PUT, 1L);
	curl_easy_setopt(curl2, CURLOPT_URL, url);
	curl_easy_setopt(curl2, CURLOPT_INFILESIZE_LARGE,64);

	curl_multi_add_handle(curlm,curl);
	curl_multi_add_handle(curlm,curl2);

	pid = fork();
	if(pid > 0)
	{
		res = curl_easy_perform(curl);
		if(res != CURLE_OK)
			printf("curl_easy_perform() failed: %s\n",curl_easy_strerror(res));
    	curl_easy_cleanup(curl);
	}
	else if (pid == 0)
	{
		res = curl_easy_perform(curl2);
		if(res != CURLE_OK)
			printf("curl_easy_perform() failed: %s\n",curl_easy_strerror(res));
    	curl_easy_cleanup(curl2);
	}

	return 0;
}
