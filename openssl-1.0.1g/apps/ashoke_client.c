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

//git test

typedef	struct	_peer_ {
	char	*peer;
	FILE	*fp;
	int		sfd;
} PEER;


PEER	PeerList[64];
int		PeerCount=0;

extern char		*optarg;
extern int		optind;
extern int		optopt;
extern int		opterr;
extern int		optreset;
extern char		*optarg;
extern SSL_CIPHER ssl3_ciphers[];
extern	int		aesni_pad_byte_test;


#define		SPACE2		"  "
#define		SPACE4		"    "
#define		SPACE6		"      "
#define		SPACE8		"        "
#define		ADMINPORT	2345

#define		DEFTIMEOUT	1000
#define		DEFLOOP		1
#define		DEFITER		1
#define		DEFBURST	1

#define		DEFCERTPATH	"/tmp/ToolPkg"

//#define		REQUEST		"GET /index.html HTTP/1.1 \r\nHost: 10.102.28.61\r\nConnection: keep-alive\r\n\r\n"

//#define		REQUEST		"GET /index.html \r\nHost: 10.102.28.61\r\nConnection: keep-alive\r\n\r\n"

#define		REQUEST	"GET /\r\n"

#define		REQLEN		strlen(REQUEST)

#define		ENDTOKEN	"I AM DONE\n"
//#define		ENDTOKEN	"</html>\n"
#define		ENDTOKLEN	strlen(ENDTOKEN)


const SSL_METHOD	*v30Method = NULL;
const SSL_METHOD	*v31Method = NULL;
const SSL_METHOD	*v32Method = NULL;
const SSL_METHOD	*v33Method = NULL;



int			printOutput	= 0;
char		*IP			= NULL;
char		*BINDIP 	= NULL;
int			PORT 		= 0;
X509		*Cert 		= NULL;
EVP_PKEY	*Key 		= NULL;
SSL_SESSION	*reuseSESS 	= NULL;
char		EndToken[32];
int			versionFilter = -1;
int			reuseCount = 0;
int			renegCount = 0;
int			logOutput = 0;
char		* logfile = NULL;
int			toutmsec   = DEFTIMEOUT;
int			iterCount = DEFITER;
int			burstSize=1;
int			burstCount=1;
int			padtest = 0;
int			padbyte = 0;
int			adminport = 0;
int			adminsock = 0;
int			recBoundary = 0;
char		*CertFile=NULL,*KeyFile=NULL;
char		*CertPath = DEFCERTPATH;
int			inetd = 0;
FILE		*errFp = NULL;
unsigned int curRandom = 0;

char		*cipherFilter = NULL;
char		*cipherSkipFilter[] = 
			{"CAMELLIA","-DSS-","SRP-","PSK-","SEED-","GOST","ECDSA",NULL};

char *vers[]	= {"ssl3","tls1","tls11","tls12",NULL};
int	 verInt[]	= {0x0300,0x0301,0x0302,0x0303,-1};

typedef char VERCIPH[16][32];
VERCIPH versionExclude[4] = 
			{
				{"SHA256","SHA384","GCM","EXP-ADH","EXP-EDH","EXP-RC2",""},
				{"SHA256","SHA384","GCM","EXP-ADH","EXP-EDH","EXP-RC2",""},
				{"SHA256","SHA384","GCM","EXP-ADH","EXP-EDH","EXP-RC2",""},
				{"EXP-","DES-CBC","ADH-AES256-GCM-SHA384","ADH-AES128-GCM-SHA256",
									"ADH-AES256-SHA256","ADH-AES128-SHA256",""}
			};


char		*CIPHERS[] = {
"AES128-SHA",
"AES128-SHA256",
"AES256-SHA",
"AES256-SHA256",
"DES-CBC-SHA",
"DES-CBC3-SHA",
"DHE-RSA-AES128-SHA",
"DHE-RSA-AES128-SHA256",
"DHE-RSA-AES256-SHA",
"DHE-RSA-AES256-SHA256",
"EDH-RSA-DES-CBC-SHA",
"EXP-DES-CBC-SHA",
"EXP-EDH-RSA-DES-CBC-SHA",
"EXP-RC2-CBC-MD5",
"EXP-RC4-MD5",
"RC4-MD5",
"RC4-SHA",
"ECDHE-RSA-AES128-SHA",
"ECDHE-RSA-AES256-SHA",
"ECDHE-RSA-DES-CBC3-SHA",
"ECDHE-RSA-RC4-SHA",
"ECDHE-RSA-AES128-SHA256",
"ECDHE-RSA-AES256-SHA384",
"AES128-GCM-SHA256",
"AES256-GCM-SHA384",
"DHE-RSA-AES128-GCM-SHA256",
"DHE-RSA-AES256-GCM-SHA384",
"ECDHE-RSA-AES128-GCM-SHA256",
"ECDHE-RSA-AES256-GCM-SHA384"
"ECDHE-RSA-AES256-GCM-SHA384",
"ADH-AES256-GCM-SHA384",
"ADH-AES256-SHA256",
"ADH-AES256-SHA",
"ADH-DES-CBC3-SHA",
"ADH-AES128-GCM-SHA256",
"ADH-AES128-SHA256",
"ADH-AES128-SHA",
"ADH-RC4-MD5",
"ADH-DES-CBC-SHA",
"EXP-ADH-DES-CBC-SHA",
"EXP-ADH-RC4-MD5",
};

int		ForEachMethod(const SSL_METHOD *);
int		ForEachCipher(const SSL_METHOD *,const SSL_CIPHER *);
char	*FailMessage(int );
void	PrintSummary(int ,const char *, char *,char *);
int		MakeSocket(char *,int );
void	AlarmHandler(int );
int		checkSkipFilter(const char *);
int		findVerInt(char *);
int  	checkVersionCipher(unsigned char ver,const char *cname);
int		callAndWait(int,const SSL_METHOD *,const SSL_CIPHER *,int (*f)(const SSL_METHOD *,const SSL_CIPHER *));
int		ForEachCipherFilter(const SSL_METHOD *M,const SSL_CIPHER *C);
int		PadTest(const SSL_METHOD *M,const SSL_CIPHER *C);
int		badPad(SSL *s,int state);
char	*FormJSONConfig();
FILE	*openPeerLog(char *peer);




extern long long test_error_inj;

main(int argc,char **argv)
{
	BIO			*in = NULL;
	RSA			*rsa = NULL;
	char	 	ch;
	char		*cert=NULL,*key=NULL;
	FILE		*fout = NULL;
	int			addrlen;
	int			sz,szlen,sd;
	int			sflag;
	struct sockaddr_in	peeraddr;
	

	struct option longopts[] = {
		{"ip",		required_argument,  		NULL,'a'},
		{"port",	required_argument, 			NULL,'b'},
		{"cert",	optional_argument,			NULL,'c'},
		{"key",		optional_argument,			NULL,'d'},
		{"version",	optional_argument,			NULL,'e'},
		{"cipher",	optional_argument,			NULL,'f'},
		{"reuse",	optional_argument,			NULL,'g'},
		{"reneg",	optional_argument,			NULL,'h'},
		{"timeout",	optional_argument,			NULL,'i'},
		{"ckv",		optional_argument,			NULL,'j'},
		{"print",	optional_argument,			NULL,'k'},
		{"log",		optional_argument,			NULL,'l'},
		{"iter",	optional_argument,			NULL,'m'},
		{"err",		optional_argument,			NULL,'n'},
		{"burst",	optional_argument,			NULL,'o'},
		{"loop",	optional_argument,			NULL,'p'},
		{"padtest",	optional_argument,			NULL,'q'},
		{"adminport",optional_argument,			NULL,'r'},
		{"inetd",	optional_argument,			NULL,'s'},
		{0,0,0,0}
	};

	optind = 0;

	InitRandom();

	while ((ch = getopt_long(argc, argv, "a:b:c:d:e:f:ghi:j:kl:m:no:p:q:r:s", longopts, NULL)) != -1)
	{
		switch(ch)
		{
			case	'a': IP = optarg;break;
			case	'b': PORT = atoi(optarg);break; 
			case	'c': cert = optarg;CertFile = cert;break;
			case	'd': key = optarg;KeyFile = key;break;
			case	'e': versionFilter = findVerInt(optarg);break;
			case	'f': cipherFilter = optarg;break;
			case	'g': reuseCount = atoi(optarg);break;
			case	'h': renegCount = 1;break;
			case	'i': toutmsec = atoi(optarg);break;
			case	'j': recBoundary = atoi(optarg);break;
			case	'k': printOutput = 1;break;
			case	'l': logOutput = 1;logfile = optarg;break;
			case	'm': iterCount = atoi(optarg);break;
			case	'n': test_error_inj |= (1 << atoi(optarg));break;
			case	'o': burstSize = atoi(optarg);break;
			case	'p': burstCount = atoi(optarg);break;
			case	'q': padtest = atoi(optarg); padbyte=8; burstCount=0;aesni_pad_byte_test=1;break;
			case	'r': adminport = atoi(optarg);break;
			case	's': inetd = 1;break;
		}
	}

	if(!inetd)
		goto no_inetd;

	if(adminport)
	{
		char	*buf;
		char	peerData[8192 * 2];
		char	ip[13];
		int		sockfd;
		int		i,ret;
		int		oneFound;
		FILE	*fp;
		struct	sockaddr_in sin;
		struct	timeval	tm;

		buf	= FormJSONConfig();

		fp = fopen("IPLIST","r");
		while(fscanf(fp,"%s",ip) > 0)
		{
			bzero(&sin,sizeof(sin));
			sin.sin_family	= AF_INET;
			sin.sin_port	= htons(adminport);
			sin.sin_addr.s_addr	= inet_addr(ip);
			sin.sin_len		= htons(sizeof(sin));
				
			sockfd = socket(PF_INET,SOCK_STREAM,6);
			if(connect(sockfd,(struct sockaddr *)&sin,sizeof(sin)) < 0)
			{
				printf("Connect to adminport failed:\n");
				exit(0);
			}

			ret = 0;
			while(ret <= strlen(buf))	
			{
				int		r;
				r	= send(sockfd,buf+ret,strlen(buf)-ret,0);
				if(r <= 0)
					break;
				ret += r;
			}

			sz = 0;
			szlen = 4;
			getsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &sz, &szlen);
			printf("size of SO_RCVBUF %d\n",sz);
			sz = 0;
			szlen = 4;
			getsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, &sz, &szlen);
			printf("size of SO_SNDBUF %d\n",sz);

			sflag = fcntl(sockfd,F_GETFL,0);
			sflag |= O_NONBLOCK;
			fcntl(sockfd,F_SETFL,sflag);
			shutdown(sockfd,SHUT_WR);
			
			PeerList[PeerCount].peer = strdup(ip);
			PeerList[PeerCount].fp = openPeerLog(ip);
			PeerList[PeerCount].sfd = sockfd;
			setbuf(PeerList[PeerCount].fp,NULL);
			PeerCount++;
		}
		//fclose(fp);
		//free(buf);


		do 
		{
		oneFound = 0;
		for(i=0;(i<PeerCount) ;i++)
		{
			if(PeerList[i].sfd == -1)
				continue;

			oneFound = 1;
			ret = recv(PeerList[i].sfd,peerData,sizeof(peerData)-1,0);
			if(ret > 0)
			{
				peerData[ret]=0;
				fprintf(PeerList[i].fp,"%s",peerData);
			}
			else if ((ret == 0) || (errno != EAGAIN))
			{
				PeerList[i].sfd = -1;
				fclose(PeerList[i].fp);
			}
		}
		} while (oneFound);
	}
	else
	{
		chdir("/tmp");
		/* Should be called from inetd */
		SetupParams(0);
		doTest();
	}
	return 0;

no_inetd:
	doTest();
}



int		ParamStrToCode(char *param)
{
	int		code = 0;

	if(strcmp(param,"ip") == 0)				code = 'a';
	else if(strcmp(param,"port") == 0)		code = 'b';
	else if(strcmp(param,"cert") == 0)		code = 'c';
	else if(strcmp(param,"key") == 0)		code = 'd';
	else if(strcmp(param,"version") == 0)	code = 'e';
	else if(strcmp(param,"cipher") == 0)	code = 'f';
	else if(strcmp(param,"reuse") == 0)		code = 'g';
	else if(strcmp(param,"reneg") == 0)		code = 'h';
	else if(strcmp(param,"timeout") == 0)	code = 'i';
	else if(strcmp(param,"ckv") == 0)		code = 'j';
	else if(strcmp(param,"print") == 0)		code = 'k';
	else if(strcmp(param,"log") == 0)		code = 'l';
	else if(strcmp(param,"iter") == 0)		code = 'm';
	else if(strcmp(param,"err") == 0)		code = 'n';
	else if(strcmp(param,"burst") == 0)		code = 'o';
	else if(strcmp(param,"loop") == 0)		code = 'p';
	else if(strcmp(param,"padtest") == 0)	code = 'q';
	else if(strcmp(param,"adminport") == 0)	code = 'r';
	else if(strcmp(param,"inetd") == 0)		code = 's';

	return code;
}

char	* FormJSONConfig()
{
	cJSON	*root, *cJ;
	char	*out = NULL;

	root	= cJSON_CreateObject();

	if(IP)
		cJSON_AddStringToObject(root,"ip", IP);

	cJSON_AddNumberToObject(root,"port", PORT);

	if(CertFile)
	{
		if((CertFile[0]=='.') && (CertFile[1]=='/'))
		{
			bcopy(CertFile+2,CertFile,strlen(CertFile)-2);
			CertFile[strlen(CertFile)-2] = 0;
		}
		cJSON_AddStringToObject(root,"cert", CertFile);
	}

	if(KeyFile)
	{
		if((KeyFile[0]=='.') && (KeyFile[1]=='/'))
		{
			bcopy(KeyFile+2,KeyFile,strlen(KeyFile)-2);
			KeyFile[strlen(KeyFile)-2] = 0;
		}
		cJSON_AddStringToObject(root,"key", KeyFile);
	}

	if(versionFilter >= 0)
		cJSON_AddNumberToObject(root,"version", versionFilter);

	if(cipherFilter)
		cJSON_AddStringToObject(root,"cipher", cipherFilter);

	if(reuseCount)
		cJSON_AddNumberToObject(root,"reuse", reuseCount);
	
	if(renegCount)
		cJSON_AddNumberToObject(root,"reneg", renegCount);

	if(toutmsec != DEFTIMEOUT)
		cJSON_AddNumberToObject(root,"timeout", toutmsec);

	if(recBoundary)
		cJSON_AddNumberToObject(root,"ckv", recBoundary);

	if(printOutput)
		cJSON_AddNumberToObject(root,"print", printOutput);

	if(logOutput)
		cJSON_AddStringToObject(root,"log", logfile);

	if(iterCount != DEFITER)
		cJSON_AddNumberToObject(root,"iter", iterCount);

	if(test_error_inj)
		cJSON_AddNumberToObject(root,"err", test_error_inj);

	if(burstSize != DEFBURST)
		cJSON_AddNumberToObject(root,"burst", burstSize);

	if(burstCount != DEFLOOP)
		cJSON_AddNumberToObject(root,"loop", burstCount);

	if(padtest)
		cJSON_AddNumberToObject(root,"padtest", padtest);

	if(adminport)
		cJSON_AddNumberToObject(root,"adminport", adminport);

	if(inetd)
		cJSON_AddNumberToObject(root,"inetd", inetd);


	out	=	cJSON_Print(root);
	cJSON_Delete(root); 
	return out;
}


int		SetupParams(int sd)
{
	char	buf[8192];
	int		buflen = 0;
	int		ret = 0;
	cJSON	*cJ, *cJc;

	char	*name;
	char	*type;
	char	*valStr;
	int		valInt;


	errFp = fopen("/tmp/tool_err","w");
	setbuf(errFp,NULL);
	bzero(buf,sizeof(buf));

	while((ret = recv(sd,buf+buflen,sizeof(buf)-buflen,0)) > 0)
	{
		buflen += ret;
	}
	
	cJ	= cJSON_Parse(buf);
	if(!cJ)
	{
		fprintf(errFp,"cJSON_Parse failed for [%s]\n",buf);
		fclose(errFp);
		exit(0);
	}


	cJc = cJ->child;
	while(cJc)
	{
		ret = ParamStrToCode(cJc->string);
		switch(ret)
		{
			case	'a': IP = strdup(cJc->valuestring);break;
			case	'b': PORT = cJc->valueint;break; 
			case	'c': CertFile = strdup(cJc->valuestring);break;
			case	'd': KeyFile = strdup(cJc->valuestring);break;
			case	'e': versionFilter = cJc->valueint;break;
			case	'f': cipherFilter = strdup(cJc->valuestring);break;
			case	'g': reuseCount = cJc->valueint;break;
			case	'h': renegCount = 1;break;
			case	'i': toutmsec = cJc->valueint;break;
			case	'j': recBoundary = cJc->valueint;break;
			case	'k': printOutput = cJc->valueint;break;
			case	'l': logOutput = 1;logfile = strdup(cJc->valuestring);break;
			case	'm': iterCount = cJc->valueint;break;
			case	'n': test_error_inj |= (1 << (cJc->valueint));break;
			case	'o': burstSize = cJc->valueint;break;
			case	'p': burstCount = cJc->valueint;break;
			case	'q': padtest = cJc->valueint; padbyte=8; burstCount=0;aesni_pad_byte_test=1;break;
			case	'r': adminport = cJc->valueint;break;
			case	's': inetd = cJc->valueint;break;
		}
		cJc = cJc->next;
	}

	return 0;
}


int		doTest()
{
	BIO		*in = NULL;
	RSA		*rsa = NULL;
	char	 ch;
	char	*cert=NULL,*key=NULL;
	FILE	*fout = NULL;
	int		adminsock = 0;
	char	filepath[256];
	char	*pwd;


	if(logOutput)
	{
		pwd = getcwd(NULL,256);
		fout = freopen(logfile,"w",stdout);
		setbuf(fout,NULL);
		if(!fout)
		{
			fprintf(errFp,"Failed to open logifile %s\n",logfile);
			exit(0);
		}
	}

	if(iterCount <= 0)
	{
		fprintf(errFp,"Bad iteration count\n");
		exit(0);
	}

	if((recBoundary < 0) || (recBoundary > 2))
	{
		fprintf(errFp,"Bad ckv\n");
		exit(0);
	}

	if(CertFile)
	{
		sprintf(filepath,"%s/%s",CertPath,CertFile);
		in = BIO_new(BIO_s_file());
		BIO_read_filename(in,filepath);
		Cert = PEM_read_bio_X509(in,NULL,NULL,NULL);
		BIO_set_close(in,BIO_CLOSE);	

		sprintf(filepath,"%s/%s",CertPath,KeyFile);
		in = BIO_new(BIO_s_file());
		BIO_read_filename(in,filepath);
		rsa = PEM_read_bio_RSAPrivateKey(in,NULL,NULL,NULL);
		Key = EVP_PKEY_new();
		EVP_PKEY_set1_RSA(Key,rsa);
		BIO_set_close(in,BIO_CLOSE);
	}

	bzero(EndToken,sizeof(EndToken));
	//setbuf(stdout,NULL);
	SSL_library_init();

	v30Method	= SSLv3_client_method();
	v31Method	= TLSv1_client_method();
	v32Method	= TLSv1_1_client_method();
	v33Method	= TLSv1_2_client_method();

	//printf("\n\nIP: %s  Port: %d\n",IP,PORT);
	//printf("-------------------------------------\n");

	while(iterCount--)
	{
		ForEachMethod(v30Method);
		ForEachMethod(v31Method);
		ForEachMethod(v32Method);
		ForEachMethod(v33Method);
	}

	if(errFp)
		fclose(errFp);
	if(fout)
		fclose(fout);
	return 0;
}


int		OpenAdminPort()
{
	int		sd = 0;
	struct	sockaddr_in	sin;

	sd = socket(PF_INET,SOCK_STREAM,6);	

	bzero(&sin,sizeof(sin));
	sin.sin_family	= AF_INET;
	sin.sin_port	= htons(adminport);
	sin.sin_addr.s_addr	= htonl(INADDR_ANY);
	sin.sin_len		= htons(sizeof(sin));

	if(bind(sd,(const struct sockaddr *)&sin,sizeof(sin)) < 0)
	{
		printf("bind to admin port failed:\n");
		return -1;
	}
	listen(sd,5);
	return sd;
}


int	ForEachMethod(const SSL_METHOD *M)
{
	int	i;
	int	numC = M->num_ciphers();
	const SSL_CIPHER	*C = NULL;

	if((versionFilter >= 0) && (M->version != versionFilter) )
		return 0;

	for(i=0;i<numC;i++)
	{
		C = M->get_cipher(i);
		if(C)
			ForEachCipherFilter(M,C);
	}
}


int	callAndWait(int num, const SSL_METHOD *M, const SSL_CIPHER *C,  int (*f)(const SSL_METHOD *M,const SSL_CIPHER *C))
{
	int	pid = getpid();
	int pidlist[1024];
	int	pidcount=0;
	int	status = 0;
	int	block=1;


	while(pid && (pidcount < num))
	{
		if(pid = fork())
			pidlist[pidcount++] = pid;
		else
		{
			f(M,C);
			exit(0);
		}
	}
	
	/*********************************
	for(pid=0;pid<num;pid++)
	{
		waitpid(pidlist[pid],&status,0);
		//printf("pid %d exited\n",pidlist[pid]);
	}
	*********************************/

	do
	{
		status = 0;
		pid = wait(&status);
	} while(pid > 0);

	return 0;
}



int	ForEachCipherFilter(const SSL_METHOD *M,const SSL_CIPHER *C)
{
	int	i;

	if(!AllowCipher(C->name,M->version))
		return 0;

	if(checkVersionCipher(M->version & 0xFF,C->name))
		return 0;

	//ForEachCipher(M,C);

	for(i=0;i<burstCount;i++)
		callAndWait(burstSize,M,C,ForEachCipher);

	if(padtest)
		PadTest(M,C);

	return 0;
}




int	PadTest(const SSL_METHOD *M,const SSL_CIPHER *C)
{
	SSL_CTX		*CTX		= SSL_CTX_new(M);
	SSL			*con		= NULL;
	char		rBuf[8092];
	int			sd, Ret=0,ecode;
	BIO			*sbio;


	CTX->cipher_list = sk_SSL_CIPHER_new_null();
	sk_SSL_CIPHER_push(CTX->cipher_list,C);	
	CTX->cipher_list_by_id = sk_SSL_CIPHER_dup(CTX->cipher_list);

	if(Cert)
		SSL_CTX_use_certificate(CTX,Cert);
	if(Key)
		SSL_CTX_use_PrivateKey(CTX,Key);

	while(padbyte)
	{
		con	= SSL_new(CTX);

		if((sd = MakeSocket(IP,PORT)) < 0)
		{
			Ret = -1;
			break;
		}
		sbio = BIO_new_socket(sd,BIO_NOCLOSE);
		SSL_set_bio(con,sbio,sbio);
		con->att.pre_enc_data = badPad;

		SSL_set_connect_state(con);
		SSL_set_no_empty_frag(con);
		ecode	= SSL_connect(con);
		if(ecode < 0)
		{
			Ret = -1;
			break;
		}

		ecode	= SSL_write(con,REQUEST,REQLEN);
		if(ecode != REQLEN)
		{
			Ret = -1;
			break;
		}

		ecode = SSL_read(con,rBuf,8090);
		if(ecode > 0)
		{
			printf("Pad Test failed..\n");
			padbyte = 0;
		}

		SSL_shutdown(con);
		sd = BIO_get_fd(con->wbio,NULL);
		close(sd);
		BIO_free(con->wbio);
	}
	if(Ret)
		printf("PadTest: Bad error\n");

	return 0;
}




int	ForEachCipher(const SSL_METHOD *M,const SSL_CIPHER *C)
{
#define	TOTERR	8
	int			reConnect 	= reuseCount;
	int			reNeg 		= renegCount;
	int			Ret			= 0;
	SSL_CTX		*CTX		= SSL_CTX_new(M);
	SSL			*con		= NULL;
	SSL_SESSION	*reuseSESS	= NULL;
	int			ecode		= 0;
	int			sd		= 0;
	char		rBuf[8092];
	int			debugLoop = 0;

	BIO			*bbio;

	/*************************************************
	if(!AllowCipher(C->name,M->version))
		return 0;

	if(checkVersionCipher(M->version & 0xFF,C->name))
		return 0;
	*************************************************/

	CTX->cipher_list = sk_SSL_CIPHER_new_null();
	sk_SSL_CIPHER_push(CTX->cipher_list,C);	
	CTX->cipher_list_by_id = sk_SSL_CIPHER_dup(CTX->cipher_list);

	if(Cert)
		SSL_CTX_use_certificate(CTX,Cert);
	if(Key)
		SSL_CTX_use_PrivateKey(CTX,Key);



	for(;;)
	{
		do 
		{
			int		sd;
			BIO		*sbio;

			con	= SSL_new(CTX);

			if(recBoundary == 1)
				SSL_set_buf_cc(con);	
			else if(recBoundary == 2)
				SSL_set_buf_cke(con);	

			if((sd = MakeSocket(IP,PORT)) < 0)
			{
				Ret = -1;
				goto end;
			}

			sbio = BIO_new_socket(sd,BIO_NOCLOSE);
			SSL_set_bio(con,sbio,sbio);

			if(reuseSESS)
				SSL_set_session(con,reuseSESS);

			SSL_set_connect_state(con);

			SSL_set_no_empty_frag(con);

			ecode	= SSL_connect(con);
			if(ecode < 0)
			{
				if(reuseSESS)
					Ret = -4;
				else
					Ret = -2;

				goto end;
			}

			if(reNeg)
				goto do_reneg;

			ecode	= SSL_write(con,REQUEST,REQLEN);
			if(ecode != REQLEN)
			{
				if(reuseSESS)
					Ret = -5;
				else
					Ret = -8;
				goto end;
			}

			bzero(EndToken,sizeof(EndToken));

			debugLoop = 0;
			for(;;)
			{
				debugLoop++;
				bzero(rBuf,8092);

				int toterr = 0;
				do
				{
					ecode = SSL_read(con,rBuf,8090);
					if(ecode > 0)
					{
						if(strcmp(rBuf+ecode-ENDTOKLEN,ENDTOKEN)==0)
							break;	
					}
					else if(ecode < 0)
						toterr++;
					else if(ecode == 0)
						toterr = TOTERR;

				} while(toterr && (toterr < TOTERR));

				if(toterr)
					break;

				//ecode = SSL_read(con,rBuf,8090);
				//if(ecode <= 0)
				//	break;


				if(printOutput)
				{
					printf("%s",rBuf);
					fflush(stdout);
				}

				rBuf[ecode] = 0;
				if(ecode >= ENDTOKLEN)
					strcpy(EndToken,rBuf+ecode-ENDTOKLEN);
				else
					strcpy(EndToken+strlen(EndToken),rBuf);

				bzero(rBuf,8092);

				if(strcmp(EndToken,ENDTOKEN) == 0)
					break;
			}

			if(!printOutput && (strcmp(EndToken,ENDTOKEN) != 0))
			{
				if(reuseSESS)
					Ret = -5;
				else
					Ret = -3;
				goto end;
			}

do_reneg:
			if(!reuseSESS)
				reuseSESS = SSL_get1_session(con);

		} while (0);

		if( (reConnect <= 0) && (reNeg <= 0) )
			break;

		if(reConnect <= 0)
		{
			reuseSESS = NULL;
			if(reNeg > 0)
			{
				SSL_renegotiate(con);
	
				if(SSL_write(con,REQUEST,REQLEN) != REQLEN)
				{
					Ret = -7;
					goto end;
				}
				bzero(EndToken,sizeof(EndToken));

				for(;;)
				{
					int	retry = 2;
					bzero(rBuf,8092);

					while(retry-- > 0)
					{
						ecode = SSL_read(con,rBuf,8090);
						if(ecode <= 0)
						{
							continue;
						}
						break;
					}
					if(ecode  <= 0)
						break;

					rBuf[ecode] = 0;
					if(ecode >= ENDTOKLEN)
						strcpy(EndToken,rBuf+ecode-ENDTOKLEN);
					else
						strcpy(EndToken+strlen(EndToken),rBuf);

					bzero(rBuf,8092);
				}

				if(strcmp(EndToken,ENDTOKEN) != 0)
				{
					Ret = -7;
					goto end;
				}

				break;
			}
		}
		else
		{
			reConnect--;
		}

	}

end:
	PrintSummary(M->version,C->name,NULL,FailMessage(Ret));

	sd = BIO_get_fd(con->wbio,NULL);
	close(sd);
	SSL_shutdown(con);
	BIO_free(con->wbio);
}


int  checkVersionCipher(unsigned char ver,const char *cname)
{
	int		i;
	char	*ptr;
	VERCIPH *name;
	name  = &versionExclude[ver];

	for(i=0;name[0][i][0];i++)
	{
		ptr = name[0][i];
		if(strstr(cname,ptr))
			return 1;
	}

	return 0;
}


char *FailMessage(int failCode)
{
	switch(failCode)
	{
		case  0: return "SUCCESS";
		case -1: return "UNREACHABLE";
		case -2: return "HANDSHAKE FAILURE";
		case -3: return "DATA READ FAILURE";
		case -4: return "REUSE HANDSHAKE FAILURE";
		case -5: return "REUSE DATA FAILURE";
		case -6: return "RENEG HANDSHAKE FAILURE";
		case -7: return "RENEG DATA FAILURE";
		case -8: return "DATA WRITE FAILURE";
		default: return "ERROR";
	}
}


void PrintSummary(int version,const char *cipher, char *options,char *result)
{
	printf("%04x%s%32s%s%32s\n",version,SPACE4,cipher,SPACE4,result);
	//fflush(stdout);
}


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

	if(toutmsec >= 1000)
	{
		tV.tv_sec	= toutmsec/1000;
	}
	tV.tv_usec	= (toutmsec % 1000) * 1000;

	setsockopt(sd,SOL_SOCKET,SO_RCVTIMEO,&tV,sizeof(tV));

	signal(SIGALRM,AlarmHandler);
	alarm(1);

	ret = connect(sd,(struct sockaddr *)&addr,sizeof(addr));

	alarm(0);
	if(ret < 0)
		return -1;
	return sd;
}

void AlarmHandler(int s)
{
}


int	AllowCipher(char *cipher, int ver)
{
	int	limit = ((ver & 0xFF) < 3) ? 22 : 28;
	int	i;
	limit = sizeof(CIPHERS)/sizeof(CIPHERS[0]);

	if(cipherFilter && strcmp(cipherFilter,cipher))
		return 0;

	for(i=0;i<limit;i++)
		if(strcmp(cipher,CIPHERS[i])==0)
			return 1;
	return 0;
}

int	checkSkipFilter(const char *cipher)
{
	int ret = 0;
	int	i;
	
	while(cipherSkipFilter[i])
	{
		if(strstr(cipher,cipherSkipFilter[i]) )
		{
			ret = 1;
			break;
		}
		i++;
	}
	
	return ret;
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


int	badPad(SSL *s,int state)
{
	SSL3_RECORD	*rec = &(s->s3->wrec);
	int	l = rec->length;
	unsigned char *ptr = rec->input;
	int	pad = rec->input[l-1];

	if(s->state != SSL_ST_OK)
		return 0;

	if(s->version == SSL3_VERSION)
	{
		ptr[l-1]++;
		padbyte = 0;
	} 
	else if(s->version == TLS1_VERSION)
	{
		ptr[l-1-padbyte]++;
		padbyte++;
	}
	else if(s->version == TLS1_2_VERSION)
	{
		ptr[l-1-padbyte]++;
		padbyte++;
	}

	if(padbyte == pad)
		padbyte = 0;

	return 0;
}



int     InitRandom()
{
    struct timeval  tv;

    gettimeofday(&tv,NULL);
    srandom(tv.tv_usec);
	curRandom = random() & 0xFFFFFFFF;
    return 0;
}


FILE	*openPeerLog(char *peer)
{
	char	filename[256];
	FILE	*fp = NULL;

	sprintf(filename,"%s.%d.log",peer,curRandom);
	fp	= fopen(filename,"w");
	//if(fp)
	//	setbuf(fp,NULL);
	return fp;
}


int		ClosePeer(int i)
{
	free(PeerList[i].peer);
	fclose(PeerList[i].fp);
	close(PeerList[i].sfd);
	bzero(&PeerList[i], sizeof(PEER));
	return 0;
}
