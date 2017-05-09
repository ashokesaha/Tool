#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <unistd.h>
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

char	*gPeerList[16];
int		gPeerNum = 0;
int		gPortList[16];
int		gPortNum = 0;

char	*gUrlList[16];
int		gUrlNum = 0;

char	*gPeerIP[64];
int		gPeerPort[64];
int		gNumPeerIpPort = 0;


CURLcode	GET_Action(char *ip, int port, char *url);
CURLcode	PUT_Action(char *ip, char *url);
int			WriteResponse(char *format, ...);
int			CloseResponse();


static size_t GET_callback(char *ptr, size_t size, size_t nmemb, void *userdata)
{
	int *p = (int *)userdata;
	*p += nmemb;
	//WriteResponse("%s",ptr);
	return nmemb;
}

static size_t GET_header_callback(char *buffer,size_t size,size_t nitems,void *userdata)
{
	if (strncmp(buffer,"Content-Length",strlen("Content-Length")) == 0)
	{
		while(*buffer++ != ':');
		*(int *)userdata = atoi(buffer);
	}
	return size * nitems;
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
	if(strcmp(param,"port") == 0) return enPORT;
	else if(strcmp(param,"cmd") == 0) return enCMD;
	else return enNONE;
}




static int	HandleArgs(char * buf)
{
	int	ret;
	cJSON	*cJ, *cJc;
	unsigned int debug = 1;
	int		i;

	
	for(i=0; i<gNumPeerIpPort; i++)
	{
		free(gPeerIP[i]);
		gPeerIP[i] = NULL;
	}
	gNumPeerIpPort = 0;

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
		if(strcmp(cJc->string,"peerlist") == 0)
		{
			int i,num = cJSON_GetArraySize(cJc);
			cJSON *cjx;
			gPeerNum = num;
			for(i=0; i<num; i++)
			{
				cjx = cJSON_GetArrayItem(cJc,i);
				gPeerList[i] = strdup(cjx->valuestring);
			}
			cJc = cJc->next;
			continue;
		}

		if(strcmp(cJc->string,"portlist") == 0)
		{
			int i,num = cJSON_GetArraySize(cJc);
			cJSON *cjx;
			gPortNum = num;
			for(i=0; i<num; i++)
			{
				cjx = cJSON_GetArrayItem(cJc,i);
				gPortList[i] = cjx->valueint;
			}
			cJc = cJc->next;
			continue;
		}

		if(strcmp(cJc->string,"urllist") == 0)
		{
			int i,num = cJSON_GetArraySize(cJc);
			cJSON *cjx;
			gUrlNum = num;
			for(i=0; i<num; i++)
			{
				cjx = cJSON_GetArrayItem(cJc,i);
				gUrlList[i] = strdup(cjx->valuestring);
			}
			cJc = cJc->next;
			continue;
		}

		if(strcmp(cJc->string,"peeripport") == 0)
		{
			cJSON *cJx = cJc->child;
			while(cJx)
			{
				gPeerIP[gNumPeerIpPort]=strdup(cJx->child->valuestring);
				gPeerPort[gNumPeerIpPort]=cJx->child->next->valueint;
				gNumPeerIpPort++;	
				cJx = cJx->next;
			}
			cJc = cJc->next;
			continue;
		}


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


	while(1)
	{
		len =  sizeof(buf) - 1;

		ret = readCmdData(0, buf, &len);
		if(ret <= 0)
			break;

		HandleArgs(buf);

		if(gCMD == mGET)
		{
			int	i,j;
			for(i=0; i<gNumPeerIpPort; i++)
				for(j=0; j<gUrlNum; j++)
					if(GET_Action(gPeerIP[i],gPeerPort[i],gUrlList[j]) != CURLE_OK)
						goto next_iter;
		}

		if(gCMD == mPUT)
		{
			int	i,j;
			for(i=0; i<gNumPeerIpPort; i++)
				for(j=0; j<gUrlNum; j++)
					PUT_Action(gPeerList[i],gUrlList[j]);
		}
next_iter:
		CloseResponse();
	}
}


CURLcode	GET_Action(char *ip, int port, char *url)
{
	CURL		*curl;
	CURLcode	res;
	char		urlstr[1024];
	long		rsvd1;
	int			val;
	int			vall = -1;
	long		totData = 0;
	
	sprintf(urlstr,"http://%s:%d/%s",ip,port,url);

	curl = curl_easy_init();
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, GET_callback);
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, &totData);
	curl_easy_setopt(curl, CURLOPT_URL, urlstr);
	val = 1;
	curl_easy_setopt(curl, CURLOPT_FAILONERROR, &val);
	curl_easy_setopt(curl, CURLOPT_STDERR, NULL);

	//curl_easy_setopt(curl, CURLOPT_HEADER, 1L);
	//curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, GET_header_callback);
	//curl_easy_setopt(curl, CURLOPT_HEADERDATA, &vall);

	curl_easy_setopt(curl, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
	curl_easy_setopt(curl, CURLOPT_TIMEOUT, 5);
	res = curl_easy_perform(curl);

	if(res != CURLE_OK)
	{
		val = -1;
		char *pp;

		curl_easy_getinfo(curl,CURLINFO_RESPONSE_CODE,&val);
		curl_easy_getinfo(curl,CURLINFO_EFFECTIVE_URL,&pp);
		WriteResponse("FaILURE [%s]: Resp code: %d ",pp,val);
    	curl_easy_cleanup(curl);
		return res;
	}
	WriteResponse("SUCCESS [%s]: Data Rcvd %d Content-Len %d ",urlstr,totData,vall);
    curl_easy_cleanup(curl);

	return 0;
}



CURLcode	PUT_Action(char *ip, char *url)
{
	CURL		*curl;
	CURLcode	res;

	sprintf(url,"http://%s:%d/",ip,(gPORT ? gPORT : 80));

	curl = curl_easy_init();
	curl_easy_setopt(curl, CURLOPT_READFUNCTION, PUT_callback);
	curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);
	curl_easy_setopt(curl, CURLOPT_PUT, 1L);
	curl_easy_setopt(curl, CURLOPT_URL, url);
	curl_easy_setopt(curl, CURLOPT_INFILESIZE_LARGE,64);
	res = curl_easy_perform(curl);

	if(res != CURLE_OK)
	{
		WriteResponse("Failure:curl_easy_perform() failed: %s\n",curl_easy_strerror(res));
    	curl_easy_cleanup(curl);
		exit(0);
	}
 
    curl_easy_cleanup(curl);
	return res;
}


int	WriteResponse(char *format, ...)
{
	char	buf[1024];
	char	tbuf[1024];
	int		len;
	va_list valist;
	
	strcpy(buf,"curlGetPut::");
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


int	CloseResponse()
{
	int		len = 0;
	fwrite((unsigned char *)&len,sizeof(len),1,stdout);
	fflush(stdout);
	return len;
}
