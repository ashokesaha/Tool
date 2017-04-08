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
int			versionFilter = -1;
int			reuseCount = 0;
int			renegCount = 0;
int			toutmsec   = DEFTIMEOUT;
int			burstSize=1;
int			burstCount=1;
int			padtest = 0;
int			nitrotest = 0;
int			padbyte = 0;
int			adminport = 0;
int			adminsock = 0;
char		*CertFile=NULL,*KeyFile=NULL;
char		*CertPath = DEFCERTPATH;
int			inetd = 0;
char		*Message = NULL;
char		*cipherFilter = NULL;
FILE		*errFp = NULL;
unsigned int curRandom = 0;

int	 verInt[]	= {0x0300,0x0301,0x0302,0x0303,-1};

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
FILE	*openPeerLog(char *peer);
int		PrintOptions();




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
		{"message",	optional_argument,			NULL,'t'},
		{0,0,0,0}
	};

	optind = 0;

	InitRandom();

	while ((ch = getopt_long(argc, argv, "a:b:c:d:e:f:ghi:j:kl:m:no:p:q:r:st:z:", longopts, NULL)) != -1)
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
			case	'k': printOutput = 1;break;
			case	'n': if(atoi(optarg)) 
							{test_error_inj |= (1 << atoi(optarg));}
						break;
			case	'o': burstSize = atoi(optarg);break;
			case	'p': burstCount = atoi(optarg);break;
			case	't': Message = strdup(optarg);break;
			case	'z': nitrotest = atoi(optarg);break;
		}
	}

	errFp = fopen("/tmp/tool_err","w");
	setbuf(errFp,NULL);
	doTest();
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


	if(CertFile)
	{
		sprintf(filepath,"%s",CertFile);
		in = BIO_new(BIO_s_file());
		BIO_read_filename(in,filepath);
		Cert = PEM_read_bio_X509(in,NULL,NULL,NULL);
		BIO_set_close(in,BIO_CLOSE);	

		sprintf(filepath,"%s",KeyFile);
		in = BIO_new(BIO_s_file());
		BIO_read_filename(in,filepath);
		rsa = PEM_read_bio_RSAPrivateKey(in,NULL,NULL,NULL);
		Key = EVP_PKEY_new();
		EVP_PKEY_set1_RSA(Key,rsa);
		BIO_set_close(in,BIO_CLOSE);
	}

	SSL_library_init();

	v30Method	= SSLv3_client_method();
	v31Method	= TLSv1_client_method();
	v32Method	= TLSv1_1_client_method();
	v33Method	= TLSv1_2_client_method();


	if(v30Method->version == versionFilter)
		ForEachMethod(v30Method);
	else if(v31Method->version == versionFilter)
		ForEachMethod(v31Method);
	else if(v32Method->version == versionFilter)
		ForEachMethod(v32Method);
	else if(v33Method->version == versionFilter)
		ForEachMethod(v33Method);

	if(errFp)
		fclose(errFp);
	if(fout)
		fclose(fout);
	return 0;
}


int	ForEachMethod(const SSL_METHOD *M)
{
	int	i;
	int	numC = M->num_ciphers();
	const SSL_CIPHER	*C = NULL;

	for(i=0;i<numC;i++)
	{
		C = M->get_cipher(i);
		if(strcmp(cipherFilter,C->name) == 0)
			break;
	}
	if(C)
		ForEachCipher(M,C);
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



int	PrintOptions()
{
	printf("IP = %s\n",IP);;
	printf("PORT = %d\n",PORT);;
	printf("CertFile = %s\n",CertFile);;
	printf("KeyFile = %s\n",KeyFile);;
	printf("versionFilter = %x\n",versionFilter);;
	printf("cipherFilter = %s\n",cipherFilter);;
	printf("reuseCount = %d\n",reuseCount);;
	printf("renegCount = %d\n",renegCount);;
	printf("toutmsec = %d\n",toutmsec);;
	printf("printOutput = %d\n",printOutput);;
	printf("test_error_inj = %x\n",test_error_inj);;
	printf("burstSize = %d\n",burstSize);;
	printf("burstCount = %d\n",burstCount);;
	printf("padtest = %d\n",padtest);;
	printf("padbyte = %d\n",padbyte);;
	printf("aesni_pad_byte_test = %d\n",aesni_pad_byte_test);;


	return 0;
}
