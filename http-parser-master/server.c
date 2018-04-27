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

#include "http_parser.h"

int 	initSocket(char *ip, int port);

int on_message_begin(http_parser *);
int on_url(http_parser *, const char *,size_t);
int on_status(http_parser *, const char *,size_t);
int on_header_field(http_parser *, const char *,size_t);
int on_header_value(http_parser *, const char *,size_t);
int on_headers_complete(http_parser *);
int on_body(http_parser *, const char *,size_t);
int on_message_complete(http_parser *);
int on_chunk_header(http_parser *);
int on_chunk_complete(http_parser *);


main(int argc, char **argv)
{
	int		sd,asd,len;
	char	buf[8 * 1024];
	http_parser				parser;
	http_parser_settings	setting;

	setting.on_message_begin = on_message_begin; 
	setting.on_url = on_url; 
	setting.on_status = on_status; 
	setting.on_header_field = on_header_field; 
	setting.on_header_value = on_header_value; 
	setting.on_headers_complete = on_headers_complete; 
	setting.on_body = on_body; 
	setting.on_message_complete = on_message_complete; 
	setting.on_chunk_header = on_chunk_header; 
	setting.on_chunk_complete = on_chunk_complete; 

	http_parser_init(&parser,HTTP_REQUEST);

	sd = initSocket(argv[1],atoi(argv[2]));
	listen(sd,5);
	asd = accept(sd,NULL,NULL);

	bzero(buf,sizeof(buf));
	while((len=read(asd,buf,8 * 1024)) > 0)
	{
		//printf("read (%d) bytes:\n", len);
		//printf("%s\n", buf);
		http_parser_execute(&parser,&setting,buf,len);
		bzero(buf,sizeof(buf));
	}
}



int 	initSocket(char *ip, int port)
{
	int	s = -1, val;
	struct sockaddr_in server;
	struct	timeval	tv;

	s = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
	memset((char *)&server,0,sizeof(server));
	server.sin_family=AF_INET;
	server.sin_port=htons((unsigned short)port);
	server.sin_addr.s_addr = INADDR_ANY;	

	val = 1;
	setsockopt(s,SOL_SOCKET,SO_REUSEADDR,&val,sizeof(val));

	bzero(&tv,sizeof(tv));
	tv.tv_sec	= 1;
	//setsockopt(s,SOL_SOCKET,SO_RCVTIMEO,&tv,sizeof(tv));

	if (bind(s,(struct sockaddr *)&server,sizeof(server)) == -1)
	{
		char	*errstr = strerror(errno);
		perror("bind::");
		s = -1;
	}

	return s;
}


int on_message_begin(http_parser *parser)
{
	printf("%s::\n",__FUNCTION__);
	return 0;
}

int on_url(http_parser *parser, const char *buf,size_t sz)
{
	char	*tbuf = strndup(buf,sz);
	printf("%s::%s\n",__FUNCTION__,tbuf);
	free(tbuf);
	return 0;
}

int on_status(http_parser *parser, const char *buf,size_t sz)
{
	printf("%s::%s\n",__FUNCTION__,buf);
	return 0;
}

int on_header_field(http_parser *parser, const char *buf,size_t sz)
{
	char	*tbuf = strndup(buf,sz);
	printf("%s::%s\n",__FUNCTION__,tbuf);
	free(tbuf);
	return 0;
}

int on_header_value(http_parser *parser, const char *buf,size_t sz)
{
	char	*tbuf = strndup(buf,sz);
	printf("%s::%s\n",__FUNCTION__,tbuf);
	free(tbuf);
	return 0;
}

int on_headers_complete(http_parser *parser)
{
	printf("%s::\n",__FUNCTION__);
	return 0;
}

int on_body(http_parser *parser, const char *buf,size_t sz)
{
	printf("%s::%s\n",__FUNCTION__,buf);
	return 0;
}

int on_message_complete(http_parser *parser)
{
	printf("%s::\n",__FUNCTION__);
	return 0;
}

int on_chunk_header(http_parser *parser)
{
	printf("%s::\n",__FUNCTION__);
	return 0;
}

int on_chunk_complete(http_parser *parser)
{
	printf("%s::\n",__FUNCTION__);
	return 0;
}
