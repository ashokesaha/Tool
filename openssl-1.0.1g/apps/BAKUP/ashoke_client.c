#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <signal.h>

#include "openssl/x509.h"
#include "openssl/ssl.h"
#include "openssl/err.h"
#include "openssl/pem.h"
#include "openssl/rand.h"
#include "openssl/ocsp.h"
#include "openssl/bn.h"


extern char		*optarg;
extern int		optind;
extern int		optopt;
extern int		opterr;
extern int		optreset;
extern char		*optarg;
extern SSL_CIPHER ssl3_ciphers[];


#define		SPACE2		"  "
#define		SPACE4		"    "
#define		SPACE6		"      "
#define		SPACE8		"        "

#define		REQUEST		"GET /index.html HTTP/1.1 \r\nHost: 10.102.28.61\r\nConnection: keep-alive\r\n\r\n"
#define		REQLEN		strlen(REQUEST)

#define		ENDTOKEN	"I AM DONE\n"
#define		ENDTOKLEN	strlen(ENDTOKEN)

const SSL_METHOD	*v30Method = NULL;
const SSL_METHOD	*v31Method = NULL;
const SSL_METHOD	*v32Method = NULL;
const SSL_METHOD	*v33Method = NULL;

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
int			toutmsec   = 1000;
char		*cipherFilter = NULL;
char		*cipherSkipFilter[] = 
			{"CAMELLIA","-DSS-","SRP-","PSK-","SEED-","GOST","ECDSA",NULL};

char *vers[]	= {"ssl3","tls1","tls11","tls12",NULL};
int	 verInt[]	= {0x0300,0x0301,0x0302,0x0303,-1};


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
};

int		ForEachMethod(const SSL_METHOD *);
int		ForEachCipher(const SSL_METHOD *,const SSL_CIPHER *);
char	*FailMessage(int );
void	PrintSummary(int ,const char *, char *,char *);
int		MakeSocket(char *,int );
void	AlarmHandler(int );
int		checkSkipFilter(const char *);
int		findVerInt(char *);




main(int argc,char **argv)
{
	BIO		*in = NULL;
	RSA		*rsa = NULL;
	char	 ch;
	char	*cert,*key;
	

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
		{0,0,0,0}
	};

	optind = 0;

	while ((ch = getopt_long(argc, argv, "a:b:c:d:e:f:ghi:", longopts, NULL)) != -1)
	{
		switch(ch)
		{
			case	'a': IP = optarg;break;
			case	'b': PORT = atoi(optarg);break; 
			case	'c': cert = optarg;break;
			case	'd': key = optarg;break;
			case	'e': versionFilter = findVerInt(optarg);break;
			case	'f': cipherFilter = optarg;break;
			case	'g': reuseCount = atoi(optarg);break;
			case	'h': renegCount = 1;break;
			case	'i': toutmsec = atoi(optarg);break;
		}
	}



	if(cert)
	{
		in = BIO_new(BIO_s_file());
		BIO_read_filename(in,cert);
		Cert = PEM_read_bio_X509(in,NULL,NULL,NULL);
		BIO_set_close(in,BIO_CLOSE);	

		in = BIO_new(BIO_s_file());
		BIO_read_filename(in,key);
		rsa = PEM_read_bio_RSAPrivateKey(in,NULL,NULL,NULL);
		Key = EVP_PKEY_new();
		EVP_PKEY_set1_RSA(Key,rsa);
		BIO_set_close(in,BIO_CLOSE);
	}

	bzero(EndToken,sizeof(EndToken));
	setbuf(stdout,NULL);
	SSL_library_init();

	v30Method	= SSLv3_client_method();
	v31Method	= TLSv1_client_method();
	v32Method	= TLSv1_1_client_method();
	v33Method	= TLSv1_2_client_method();


	ForEachMethod(v30Method);
	ForEachMethod(v31Method);
	ForEachMethod(v32Method);
	ForEachMethod(v33Method);
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
			ForEachCipher(M,C);
	}
}


int	ForEachCipher(const SSL_METHOD *M,const SSL_CIPHER *C)
{
	int			reConnect 	= reuseCount;
	int			reNeg 		= renegCount;
	int			Ret			= 0;
	SSL_CTX		*CTX		= SSL_CTX_new(M);
	SSL			*con		= NULL;
	SSL_SESSION	*reuseSESS	= NULL;
	int			ecode		= 0;
	char		rBuf[8092];


	if(!AllowCipher(C->name,M->version))
		return 0;

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

			ecode	= SSL_connect(con);
			if(ecode < 0)
			{
				if(reuseSESS)
					Ret = -4;
				else
					Ret = -2;

				goto end;
			}


			ecode	= SSL_write(con,REQUEST,REQLEN);
			if(ecode != REQLEN)
			{
				if(reuseSESS)
					Ret = -5;
				else
					Ret = -3;
				goto end;
			}

			bzero(EndToken,sizeof(EndToken));

			for(;;)
			{
				bzero(rBuf,8092);
				ecode = SSL_read(con,rBuf,8090);
				if(ecode <= 0)
				{
					break;
				}

				rBuf[ecode] = 0;
				if(ecode >= ENDTOKLEN)
					strcpy(EndToken,rBuf+ecode-ENDTOKLEN);
				else
					strcpy(EndToken+strlen(EndToken),rBuf);

				bzero(rBuf,8092);
			}

			if(strcmp(EndToken,ENDTOKEN) != 0)
			{
				if(reuseSESS)
					Ret = -5;
				else
					Ret = -3;
				goto end;
			}

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
					bzero(rBuf,8092);
					ecode = SSL_read(con,rBuf,8090);
					if(ecode <= 0)
					{
						break;
					}

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
}



char *FailMessage(int failCode)
{
	switch(failCode)
	{
		case  0: return "SUCCESS";
		case -1: return "UNREACHABLE";
		case -2: return "HANDSHAKE FAILURE";
		case -3: return "DATA FAILURE";
		case -4: return "REUSE HANDSHAKE FAILURE";
		case -5: return "REUSE DATA FAILURE";
		case -6: return "RENEG HANDSHAKE FAILURE";
		case -7: return "RENEG DATA FAILURE";
		default: return "ERROR";
	}
}


void PrintSummary(int version,const char *cipher, char *options,char *result)
{
	printf("%04x%s%32s%s%32s\n",version,SPACE4,cipher,SPACE4,result);
	fflush(stdout);
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

	if(cipherFilter && strcmp(cipherFilter,cipher))
		return 0;

	for(i=0;i<=limit;i++)
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
