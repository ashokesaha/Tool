#include <stdio.h>
#include <unistd.h>
#include <getopt.h>

extern char *optarg;
extern int optind;
extern int optopt;
extern int opterr;
extern int optreset;

char *vers[]	= {"ssl3","tls1","tls11","tls12",NULL};
int	 verInt[]	= {0,1,2,3,4,-1};

int	findVerInt(char *v);

main(int argc,char **argv)
{
	int		aa = 0;
	int		ch,idx;
	
	char	*ip;
	char	*cipher;
	char	*certfile = NULL;
	char	*keyfile = NULL;
	int		port;
	int		version;

	struct option longopts[] = {
		{"ip",		required_argument,  		NULL,'a'},
		{"port",	required_argument, 			NULL,'b'},
		{"cert",	optional_argument,			NULL,'c'},
		{"key",		optional_argument,			NULL,'d'},
		{"version",	optional_argument,			NULL,'e'},
		{"cipher",	optional_argument,			NULL,'f'},
		{0,0,0,0}
	};

	idx = 0;
	optind = 0;

	while ((ch = getopt_long(argc, argv, "a:b:cdef", longopts, NULL)) != -1)
	{
		idx++;
		switch(ch)
		{
			case	'a': ip = optarg;break;
			case	'b': port = atoi(optarg);break; 
			case	'c': certfile = optarg;break;
			case	'd': keyfile = optarg;break;
			case	'e': version = findVerInt(optarg);break;
			case	'f': cipher = optarg;break;
		}
	}

	printf("ip		: %s\n",ip);
	printf("port	: %d\n",port);
	printf("cert	: %s\n",certfile);
	printf("key		: %s\n",keyfile);
	printf("version	: %d\n",version);
	printf("cipher	: %s\n",cipher);
}


int	findVerInt(char *v)
{
	int	i;
	for(i=0;vers[i];i++)
	{
		if(strcmp(vers[i],v) == 0)
			return verInt[i];
	}
	return -1;
}
