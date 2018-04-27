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

#include <sys/wait.h>
#include <sys/time.h>
#include <openssl/ossl_typ.h>
#include <openssl/bio.h>
#include <openssl/ssl.h>
#include <openssl/dh.h>
#include <openssl/ec.h>
#include <openssl/bio.h>
#include <openssl/x509v3.h>
#include <openssl/err.h>
#include <sys/select.h>
#include "cJSON.h"

#if 0
#define		REQUEST		"GET /index.html HTTP/1.1\r\nHost: 10.102.28.72\r\nConnection: keep-alive\r\n\r\n"

#define		REQUEST		"GET /index.html HTTP/1.1\r\nHost: 10.102.28.72\r\nConnection: keep-alive\r\nASHOKEHDR: TEST1\r\n\r\n"
#endif

#define		REQUEST		"GET /index.html HTTP/1.1\r\nHost: 10.102.28.72\r\nConnection: close\r\nASHOKEHDR: TEST1\r\n\r\n"


#define		REQLEN		strlen(REQUEST)

#define		ENDTOKEN	"I AM DONE\n"
#define		ENDTOKLEN	strlen(ENDTOKEN)
#define		CLIENTHOME	"/mnt/ToolPkg/Client/"
#define		MAXCHILD	4

#define		STATUS_CAUTH	0x01

typedef struct _child_stat_ {
	int							id;
	int							rescount;
	int 						pid;
	int							pass;
	int							fail;
	char						childLogFile[64];
	unsigned	int				rsapadtest;
	char						*testid;
	struct 		_child_stat_	*next;	
} CHILD_STAT_t;

typedef struct _cert_list_ {
	X509		*s_cert;
	EVP_PKEY	*s_key;
	char		*sigalg;
	int			keysize;
} CERT_LIST_t;



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
"EXP-ADH-RC4-MD5"
};

static int			doTest();
static int			ForEachMethod(const SSL_METHOD *);
static int			ForEachCipherFilter(const SSL_METHOD *,const SSL_CIPHER *);
static int			ForEachCipher(const SSL_METHOD *,const SSL_CIPHER *,int,unsigned int *);
static int  		checkVersionCipher(unsigned char,const char *);
static int 			SendResult(SSL *,char *,const SSL_CIPHER *);
static int			MakeSocket(char *,int );
static int			AllowCipher(const char *,int);
static int			checkSkipFilter(const char *);
static int			CleanChild();
static int			HandleArgs(char *);
static int	 		readCmdData(int ,unsigned char *, int *);
static int			WriteResponse(char *format, ...);
static int  		WaitForChild(int);
static int 			CloseResponse();
static int			findVerInt(char *);
static char 		*JsonTest();
static cJSON 		*MakeJson(int ,int ,char *);
static int  		BigJson();
static int			loadCertsByPrefix(char *);
static int			AddCertByName(char *,char *);
static int			StreamFileByLine(char *file);
static int			StreamResults(char *);
int			FillCommonNames(X509 *x509, char *out);

extern	int				GetServerCertDetails(SSL *,char *,char *);
extern	DH				*SSL_get_dh(SSL *s);
extern	DH				*SSL_get_peerdh(SSL *s);
extern  X509			*ssl_get_server_send_cert(const SSL *s);
extern	char			*SSL_get_curvename(SSL *s);
extern	unsigned short 	SSL_get_peer_port(SSL *s);
extern	int 			SSL_set_peer_port(SSL *s, unsigned short port);
extern	char			*get_ecc_curvename(SSL *s);
extern	char			*ASHOKE_TOOL_get_cert_info(X509 *,char *);
extern	char			*ASHOKE_TOOL_get_ecc_info(SSL *);
extern	int				ASHOKE_TOOL_write_session(SSL *, char *);
extern	SSL_SESSION		*ASHOKE_TOOL_find_session(unsigned char *, char *);



CHILD_STAT_t			*childStatQ = NULL;
CHILD_STAT_t 			*curChildStat = NULL;
CHILD_STAT_t			*childStatFreeQ = NULL;
CHILD_STAT_t			*childStatActiveQ = NULL;

char					*IP = NULL;
int						PORT = 0;
int						REUSE = 0;
int						RENEG = 0;
int						CAUTH = 0;
int						RECBOUNDARY = 0;
int						ITERCOUNT = 0;
int						CHILDCOUNT = 1;
int						REQSIZE = 0;
int						RECSIZE = 0;
int						DELAY = 0;
int						VERSIONFILTER = 0;
char					*CIPHERFILTER = NULL;
char					*CERTFILE = NULL;
char					*KEYFILE = NULL;
char					*CERTLINK = NULL;
char					*SERVERNAME = NULL;
int						CHILDID = 1;
int						RSAPADTEST = 0;
int						TOUTMSEC = 3000;
char					EndToken[32];
int						padtest = 0;
int						smallrecordtest = 0;
cJSON					*cjArray;
char					*respBuf = NULL;
char					*TESTID_str = NULL;
FILE					*debugParentFP = NULL;
FILE					*debugChildFP = NULL;

const SSL_METHOD		*v30Method = NULL;
const SSL_METHOD		*v31Method = NULL;
const SSL_METHOD		*v32Method = NULL;
const SSL_METHOD		*v33Method = NULL;

CERT_LIST_t				gCertList[1024];
int						gNumCertKey = 0;
int						filedes[2];

extern unsigned int TESTVAR_rsapadtest;

int main(int argc, char **argv)
{
	int						sd;
	int						len, childCount=0;
	int						i,pid = -1;
	int						status = 0, ret;
	int						curCert,curDH,curMethod,curCiphIdx;
	char					namebuf[256];
	char					buf[1024];
	const SSL_METHOD		*meth;
	const SSL_CIPHER		*cipher;
	DH						*dh;
	EC_KEY					*ecKey;
	X509					*cert;
	EVP_PKEY				*pkey;
	CHILD_STAT_t			*tChildStat;
	struct	sockaddr_in		from;
	fd_set					readfds;
	struct	timeval			tv;
	volatile int			main_debug = 1;
	char					fpname[32];

	volatile int debugmain=1;

	TESTVAR_rsapadtest = 0;

	chdir("/tmp");
	sprintf(fpname,"/tmp/debug.client.%d",getpid());
	debugParentFP = fopen(fpname,"w");
	setbuf(debugParentFP,NULL);


	respBuf = malloc(256 * 1024);

	len =  sizeof(buf) - 1;
	ret = readCmdData(0, buf, &len);
	if(ret <= 0)
		return 0;

	if(strcmp(buf,"twinkletwinkle"))
		return 0;
	WriteResponse("%s","upabovethe");


	for(ret=0; ret < MAXCHILD; ret++)
	{
		tChildStat = (CHILD_STAT_t *)malloc(sizeof(CHILD_STAT_t));
		tChildStat->pid = 0;
		tChildStat->id = ret;
		tChildStat->rescount = 0;
		tChildStat->next = childStatFreeQ;
		childStatFreeQ = tChildStat;
	}

	tv.tv_sec = 0;
	tv.tv_usec = 500 * 1024;
	pipe(filedes);

	while(1)
	{
		FD_ZERO(&readfds);
		FD_SET(0,&readfds);

		select(1,&readfds,NULL,NULL,&tv);
	
		if(FD_ISSET(0,&readfds))
		{
			len =  sizeof(buf) - 1;
			ret = readCmdData(0, buf, &len);
			if(ret <= 0)
				break;
			fprintf(debugParentFP,"readCmdData read [%s]\n",buf);

			HandleArgs(buf);

			for(ret=0; ret < CHILDCOUNT ; ret++)
			{
				curChildStat		= childStatFreeQ;
				childStatFreeQ		= childStatFreeQ->next;
				curChildStat->next	= childStatActiveQ;
				childStatActiveQ	= curChildStat;
				curChildStat->pass  = curChildStat->fail=curChildStat->pid=0;
				curChildStat->id  = 	CHILDID++;
				curChildStat->rsapadtest  = 	TESTVAR_rsapadtest;
				curChildStat->testid  = 	TESTID_str;
				sprintf(curChildStat->childLogFile,"/tmp/debug.client.%s.%d",TESTID_str,ret);

				pid = fork();

				if(pid > 0)
				{
					int i = 1;
					fprintf(debugParentFP,"created child %d\n",pid);
					curChildStat->pid = pid;
					write(filedes[1],&i,sizeof(i));
				}
				else if (pid == 0)
				{
					int pid,status;
					int i = 0;
					volatile int debug = 1;
					debugChildFP = fopen(curChildStat->childLogFile,"w");
					read(filedes[0],&i,sizeof(i));

					if(!ITERCOUNT)
						ITERCOUNT=1;
					for(i=0; i<ITERCOUNT; i++)
					{
						pid = fork();
						if (pid > 0)
						{
							waitpid(pid,&status,0);
						}
						else if (pid == 0)
						{
							ret = doTest();
							exit(0);
						}
						else
							break;
					}

					fclose(debugChildFP);
					debugChildFP = NULL;
					exit(ret);
				}
				else
				{
					goto Exit;
				}
			}

			tv.tv_sec = 1;
			tv.tv_usec = 0;
			while(childStatActiveQ)
			{
				CleanChild();

				FD_ZERO(&readfds);
				FD_SET(0,&readfds);
				select(1,&readfds,NULL,NULL,&tv);
				if(FD_ISSET(0,&readfds))
				{
					len =  sizeof(buf) - 1;
					ret = readCmdData(0, buf, &len);
					if(ret <= 0)
					{
						WaitForChild(1);
						break;
					}
				}
			}

			fprintf(debugParentFP,"sending ENDD\n");
			fflush(debugParentFP);
			WriteResponse("%s","ENDD");
		}
	}

Exit:
	fprintf(debugParentFP,"Exiting . Killing child\n");
	fflush(debugParentFP);
	WaitForChild(1);
	fprintf(debugParentFP,"Exiting . Killed child\n");
}



static int doTest()
{
	BIO		*in = NULL;
	RSA		*rsa = NULL;
	char	 ch;
	char	*cert=NULL,*key=NULL;
	FILE	*fout = NULL;
	int		adminsock = 0;
	char	filepath[256];
	char	*pwd;
	int		iterCount = 0;
	char	*out = NULL;
	char	fpname[32];

	volatile int debug = 1;

	curChildStat->rescount = 0;

	chdir("/mnt/ToolPkg/Client");
	if(CERTFILE)
	{
		loadCertsByPrefix(CERTFILE);
	}
	chdir("/tmp");

	cjArray	= cJSON_CreateArray();

	if(ITERCOUNT)	
		iterCount = ITERCOUNT;
	else
		iterCount = 1;

	bzero(EndToken,sizeof(EndToken));
	SSL_load_error_strings();
	ERR_load_crypto_strings();
	SSL_library_init();

	v30Method	= SSLv3_client_method();
	v31Method	= TLSv1_client_method();
	v32Method	= TLSv1_1_client_method();
	v33Method	= TLSv1_2_client_method();

	/* we have crashes when client runs for a long time. As a stop gap
	 * each client would run one iteration and we shall fork many clients.
	 */
	iterCount=1;
	while(iterCount--)
	{
		ForEachMethod(v30Method);
		ForEachMethod(v31Method);
		ForEachMethod(v32Method);
		ForEachMethod(v33Method);
	}

	return 0;
}



static int	ForEachMethod(const SSL_METHOD *M)
{
	int	i;
	int	numC = M->num_ciphers();
	const SSL_CIPHER	*C = NULL;

	if((VERSIONFILTER > 0) && (M->version != VERSIONFILTER) )
		return 0;

	for(i=0;i<numC;i++)
	{
		C = M->get_cipher(i);
		if(C)
			ForEachCipherFilter(M,C);
	}
}



static int	ForEachCipherFilter(const SSL_METHOD *M,const SSL_CIPHER *C)
{
	int	i,k;
	unsigned int status;

	if(!AllowCipher(C->name,M->version))
		return 0;

	if(checkVersionCipher(M->version & 0xFF,C->name))
		return 0;
		
	k = 0;
	do
	{
		if(curChildStat->rsapadtest)
		{
			status = 0;
			TESTVAR_rsapadtest = 1;
			ForEachCipher(M,C,k,&status);

			status = 0;
			TESTVAR_rsapadtest = 2;
			ForEachCipher(M,C,k,&status);

			status = 0;
			TESTVAR_rsapadtest = 8;
			ForEachCipher(M,C,k,&status);
		}
		else
		{
			status = 0;
			ForEachCipher(M,C,k,&status);
		}
		k++;

		if(!(status & STATUS_CAUTH))
			k = gNumCertKey;

	} while(k<gNumCertKey);

	return 0;
}




static int	ForEachCipher(const SSL_METHOD *M,const SSL_CIPHER *C,int certIndex, unsigned int *attr)
{
#define	TOTERR	8
	int			reConnect 	= REUSE;
	int			reNeg 		= RENEG;
	int			Ret			= 0;
	SSL_CTX		*CTX		= SSL_CTX_new(M);
	SSL			*con		= NULL;
	SSL_SESSION	*reuseSESS	= NULL;
	X509		*Cert 		= NULL;
	EVP_PKEY	*Key 		= NULL;
	BIO			*bbio, *in;
	RSA			*rsa;
	EVP_PKEY	*pkey;
	CERT_LIST_t	*cert;
	int			ecode		= 0;
	int			sd			= 0;
	char		rBuf[8092];
	int			debugLoop 	= 0;
	char		*status		= "Success";
	char		filepath[128];
	char		*certCN = NULL;
	char		serverCN[128],certType[16];

	volatile int mydebug=1;

	if(CERTLINK)
	{
		int ret;
		ret = SSL_CTX_load_verify_locations(CTX,CERTLINK,NULL);
	}

	CTX->cipher_list = sk_SSL_CIPHER_new_null();
	sk_SSL_CIPHER_push(CTX->cipher_list,C);	
	CTX->cipher_list_by_id = sk_SSL_CIPHER_dup(CTX->cipher_list);

	cert = &gCertList[certIndex];
	if(cert && cert->s_cert)
	{
		X509_NAME *name;
		char buf[128];
		char	*ptr,*ptr2;
		name = X509_get_subject_name(cert->s_cert);
		X509_NAME_oneline(name,buf,127);
		ptr = strstr(buf,"CN=");
		if(ptr)
		{
			ptr2 = ptr;
			while(*ptr2 != '/') ptr2++;
			if(*ptr2) *ptr2 = 0;
			certCN = strdup(ptr);
		}

		SSL_CTX_use_certificate(CTX,cert->s_cert);
		SSL_CTX_use_PrivateKey(CTX,cert->s_key);
	}

	if(CERTLINK)
	{
		int ret;
		ret = SSL_CTX_load_verify_locations(CTX,CERTLINK,NULL);
	}


	for(;;)
	{
		int		sd = 0;
		BIO		*sbio = NULL;

		do 
		{
			con	= SSL_new(CTX);

			if(RECBOUNDARY == 1)
				SSL_set_buf_cc(con);	
			else if(RECBOUNDARY == 2)
				SSL_set_buf_cke(con);	
			else if(RECBOUNDARY == 3)
				SSL_set_buf_ckeccv(con);	

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

			if(SERVERNAME)
				SSL_set_tlsext_host_name(con,SERVERNAME);

			ecode	= SSL_connect(con);

			{
				struct sockaddr_in sin;
				int	sinlen = sizeof(sin);
				getsockname(sd,(struct sockaddr *)&sin,&sinlen);
				SSL_set_peer_port(con,ntohs(sin.sin_port));
			}

			if(con->s3->tmp.cert_req)
				*attr |= STATUS_CAUTH;	

			GetServerCertDetails(con,serverCN,certType);
			if(ecode <= 0)
			{
				unsigned long l;
				char	*ptr;
				l = ERR_get_error();
				ptr = ERR_error_string(l,NULL);

				status = "Handshake Failure";
				if(reuseSESS)
					Ret = -4;
				else
					Ret = -2;

				SendResult(con,ptr,C);

				sd = BIO_get_fd(con->wbio,NULL);
				close(sd);
				SSL_shutdown(con);
				BIO_free(con->wbio);
				goto end;
			}

			if(reuseSESS && !con->hit)
			{
				status = "Reuse Failure";
				SendResult(con,status,C);
				Ret = -4;
				sd = BIO_get_fd(con->wbio,NULL);
				close(sd);
				SSL_shutdown(con);
				BIO_free(con->wbio);
				goto end;
			}

			if(reNeg)
				goto do_reneg;

			ecode	= SSL_write(con,REQUEST,REQLEN);
			if(ecode != REQLEN)
			{
				status = "Write Failure";
				SendResult(con,status,C);
				if(reuseSESS)
					Ret = -5;
				else
					Ret = -8;

				sd = BIO_get_fd(con->wbio,NULL);
				close(sd);
				SSL_shutdown(con);
				BIO_free(con->wbio);
				goto end;
			}

			bzero(EndToken,sizeof(EndToken));

			debugLoop = 0;

			while(1)
			{
				ecode = SSL_read(con,rBuf,8090);
				if(ecode > 0)
				{
					rBuf[ecode] = 0;
					if(ecode >= ENDTOKLEN)
						strcpy(EndToken,rBuf+ecode-ENDTOKLEN);
					else
					{
						char	tmpToken[64] = "";
						int		tlen=0;
						strcat(EndToken,rBuf);
						tlen = strlen(EndToken);
						if(tlen > ENDTOKLEN)
						{
							strcpy(tmpToken,EndToken+(tlen-ENDTOKLEN));
							strcpy(EndToken,tmpToken);
						}
					}
					if(strcmp(EndToken,ENDTOKEN) == 0)
						break;
				}
				else
				{
					if(SSL_get_error(con,ecode) == SSL_ERROR_WANT_READ)
					{
						fprintf(debugChildFP,"Sleeping... %d\n",SSL_get_peer_port(con));
						fflush(debugChildFP);
						
						sleep(1);
					}
					else
						break;
				}
			}

#if 0
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
					{
						toterr++;
						break;
					}
					sleep(1);

					/* if ecode is 0, not considering it error first time.
					 * But after sleeping for 1 second, expect the data to
					 * be present and dont expect a ecode 0
					 */

					/*****************************************
					while(1)
					{
						ecode = SSL_read(con,rBuf,8090);
						if(ecode <= 0)
						{
							if(SSL_get_error(con,ecode) == SSL_ERROR_WANT_READ)
								sleep(1);
							else
								break;
						}
					}
					*****************************************/

					ecode = SSL_read(con,rBuf,8090);
					if(ecode <= 0)
					{
						toterr++;
						break;
					}
				} while(toterr && (toterr < TOTERR));


				if(toterr)
				{
					Ret = -1;
					fprintf(debugChildFP,"Peer port %d\n",SSL_get_peer_port(con));
					fflush(debugChildFP);
					status = "Read Failure 1";
					SendResult(con,status,C);
					goto end;
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
#endif

			if(strcmp(EndToken,ENDTOKEN) != 0)
			{
				struct sockaddr_in peer;
				int peerlen;

				status = "Read Failure 2";
				SendResult(con,status,C);
				if(reuseSESS)
					Ret = -5;
				else
					Ret = -3;

				peerlen =  sizeof(peer);
				getsockname(sd,(struct sockaddr *)&peer,&peerlen);

				//close(sd);
				//SSL_shutdown(con);
				//BIO_free(con->wbio);
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
					SendResult(con,"Reneg Write Failure",C);
					Ret = -7;
					sd = BIO_get_fd(con->wbio,NULL);
					close(sd);
					SSL_shutdown(con);
					BIO_free(con->wbio);
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
					SendResult(con,"Reneg Read Failure",C);
					Ret = -7;
					sd = BIO_get_fd(con->wbio,NULL);
					close(sd);
					SSL_shutdown(con);
					BIO_free(con->wbio);
					goto end;
				}

				break;
			}
		}
		else
		{
			reConnect--;
		}

	sd = BIO_get_fd(con->wbio,NULL);
	close(sd);
	SSL_shutdown(con);
	SSL_free(con);
	}

end:
	if(Ret == 0)
		SendResult(con,"Success",C);
	else
	{
		SSL_shutdown(con);
		sd = BIO_get_fd(con->wbio,NULL);
		close(sd);
		BIO_free(con->wbio);
	}
	SSL_CTX_free(CTX);
	return 0;
}



static int  checkVersionCipher(unsigned char ver,const char *cname)
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


static int SendResult(SSL *ssl,char *status,const SSL_CIPHER *C)
{
	cJSON	*root, *cJ,*cjArray;
	DH		*dh;
	char	*ecname,*out = NULL;
	char	buf[1024];
	char	tbuf[1024];
	X509	*x509;
	int		i;
	
	struct rlimit rlp;
	getrlimit(RLIMIT_AS,&rlp);
	//fprintf(debugChildFP,"rlimit: %x\n",rlp.rlim_cur);
	//fflush(debugChildFP);
	

	curChildStat->rescount++;
	root	= cJSON_CreateObject();

	sprintf(buf,"0x%x",SSL_version(ssl));
	cJSON_AddStringToObject(root,"version", buf);

	if(ssl->session && ssl->session->cipher)
		cJSON_AddStringToObject(root,"cipher",SSL_get_current_cipher_name(ssl));
	else
		cJSON_AddStringToObject(root,"cipher", C->name);

	tbuf[0] = 0;
	if(ssl->s3->tmp.cert_req && ssl->s3->tmp.new_cipher && (x509=ssl_get_server_send_cert(ssl)))
		ASHOKE_TOOL_get_cert_info(x509,tbuf);
	else
		strcpy(tbuf,"None");
	cJSON_AddStringToObject(root,"ClientCert", tbuf);

	tbuf[0] = 0;
	if(ssl->session->peer)
		ASHOKE_TOOL_get_cert_info(ssl->session->peer,tbuf);
	else
		strcpy(tbuf,"None");
	cJSON_AddStringToObject(root,"ServerCert", tbuf);

	tbuf[0] = 0;
	out = SSL_get_servername(ssl,TLSEXT_NAMETYPE_host_name);
	if(out)
		strcpy(tbuf,out);
	else
		strcpy(tbuf,"None");
	cJSON_AddStringToObject(root,"SNI", tbuf);

	
	tbuf[0] = 0;
	FillCommonNames(ssl->session->peer, tbuf);
	cJSON_AddStringToObject(root,"Server CN", tbuf);


	tbuf[0] = 0;
	if((dh=SSL_get_peerdh(ssl)))
	{
		sprintf(tbuf,"%d", BN_num_bits(dh->p));
	}
	else
		strcpy(tbuf,"None");
	cJSON_AddStringToObject(root,"DH", tbuf);

	if((ecname=get_ecc_curvename(ssl)))
	{
		sprintf(tbuf, "%s", ecname);
	}
	else
		strcpy(tbuf,"None");
	cJSON_AddStringToObject(root,"ECC", tbuf);


	if(ssl->hit)
		i = 1;
	else
		i = 0;
	cJSON_AddNumberToObject(root,"reuse", i);
	

	if(ssl->new_session)
		i = 1;
	else
		i = 0;
	cJSON_AddNumberToObject(root,"reneg", i);

	sprintf(buf,"%d",TESTVAR_rsapadtest);
	cJSON_AddStringToObject(root,"rsapadtest",buf); 

	cJSON_AddNumberToObject(root,"a", curChildStat->rescount);


	cJSON_AddStringToObject(root,"result", status);

	cjArray = cJSON_CreateArray();
	cJSON_AddItemToArray(cjArray,root);
	out	=	cJSON_PrintUnformatted(root);
	fprintf(debugChildFP,"%s\n",out);
	fflush(debugChildFP);
	cJSON_Delete(cjArray);

	return 0;
}




static char * JsonTest()
{
	cJSON	*root, *cJ;
	char	*out = NULL;

	root	= cJSON_CreateObject();
	cJSON_AddStringToObject(root,"ip", "10.102.28.72");
	cJSON_AddNumberToObject(root,"port", 4343);
	cJSON_AddNumberToObject(root,"childcount", 2);
	cJSON_AddStringToObject(root,"version", "tls1");
	out	=	cJSON_Print(root);
	return out;
}


static cJSON *MakeJson(int v1, int v2, char *str)
{
	cJSON	*root;
	root	= cJSON_CreateObject();
	cJSON_AddNumberToObject(root,"v1", v1);
	cJSON_AddNumberToObject(root,"v2", v2);
	cJSON_AddStringToObject(root,"v3", str); 
	return root;
}

static int  BigJson()
{
	cJSON	*root, *r1;
	char	*out;

	root	= cJSON_CreateArray();
	r1 = MakeJson(1,2,"12");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(3,4,"34");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);
	r1 = MakeJson(5,6,"56");
	cJSON_AddItemToArray(root,r1);

	out = cJSON_Print(root);
	cJSON_Delete(root);
	printf("%s\n",out);
	free(out);
	return 0;
}


static int	MakeSocket(char *ip,int port)
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



static int	AllowCipher(const char *cipher, int ver)
{
	int	limit = ((ver & 0xFF) < 3) ? 22 : 28;
	int	i;
	limit = sizeof(CIPHERS)/sizeof(CIPHERS[0]);


	if(CIPHERFILTER && !strstr(cipher,CIPHERFILTER))
		return 0;

	for(i=0;i<limit;i++)
		if(strcmp(cipher,CIPHERS[i])==0)
			return 1;
	return 0;
}


static int	checkSkipFilter(const char *cipher)
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


static int	loadCertsByPrefix(char *prefix)
{
	char	certName[64];
	char	keyName[64];
	int		i,j,k, x,max;
	int		ret;

	struct	stat sb;
	BIO		*cert;
	BIO		*key;

	int		keysize[] = {1024,2048,4096};
	int		mdsize[] = {1,256,384};

	for(x = 0; x < sizeof(gCertList)/sizeof(gCertList[0]); x++)
	{
		gCertList[x].s_cert = NULL;
		gCertList[x].s_key  = NULL;
	}

	max = x;

	if(CERTFILE && KEYFILE)
	{
		if( (stat(CERTFILE,&sb)!=-1) && (stat(KEYFILE,&sb)!=-1) )
			return AddCertByName(CERTFILE,KEYFILE);
	}
	

	for(i=0; i< sizeof(keysize)/sizeof(keysize[0]); i++)
	for(j=0; j< sizeof(mdsize)/sizeof(mdsize[0]); j++)
	{
		bzero(certName,sizeof(certName));
		bzero(keyName,sizeof(keyName));

		sprintf(certName,"client%d_sha%d_cert.pem",keysize[i],mdsize[j]);
		sprintf(keyName,"client%d_sha%d_key.pem",keysize[i],mdsize[j]);

		if((stat(certName,&sb)==-1) || (stat(keyName,&sb)==-1))
		{
			break;
		}

		if(ret=AddCertByName(certName,keyName) <= 0)
			break;
	}

	return ret;
}


static int	AddCertByName(char *certName,char *keyName)
{
	BIO			*cert;
	BIO			*key;
	BIO			*bp;
	X509		*x509;
	EVP_PKEY	*pkey;
	int			ret = 0;
	char		*ptr = getcwd(NULL,0);

	if ((cert=BIO_new(BIO_s_file())) == NULL)
		return 0;
	if ((key=BIO_new(BIO_s_file())) == NULL)
	{
		BIO_free(cert);
		return 0;
	}

	if (BIO_read_filename(cert,certName) <= 0)
	{
		BIO_free(cert);
		BIO_free(key);
		return 0;
	}
	if (BIO_read_filename(key,keyName) <= 0)
	{
		BIO_free(cert);
		BIO_free(key);
		return 0;
	}

	if( !(x509 = PEM_read_bio_X509_AUX(cert,NULL,NULL,NULL)) )
	{
		BIO_free(cert);
		BIO_free(key);
		return 0;
	}

	if( !(pkey = PEM_read_bio_PrivateKey(key,NULL,NULL,NULL)))
	{
		X509_free(x509);
		BIO_free(cert);
		BIO_free(key);
		return 0;
	}

	gCertList[gNumCertKey].s_cert = x509;
	gCertList[gNumCertKey].s_key  = pkey; 

	pkey = X509_get_pubkey(x509);
	bp = BIO_new(BIO_s_mem());
	gCertList[gNumCertKey].keysize = EVP_PKEY_bits(pkey);
	EVP_PKEY_free(pkey);
	gCertList[gNumCertKey].sigalg = malloc(32);
	X509_signature_print(bp,x509->sig_alg,NULL);
	BIO_gets(bp,gCertList[gNumCertKey].sigalg,31);
	if(gCertList[gNumCertKey].sigalg[strlen(gCertList[gNumCertKey].sigalg)-1] == '\n')
		gCertList[gNumCertKey].sigalg[strlen(gCertList[gNumCertKey].sigalg)-1] = 0;	
	BIO_free(bp);

	gNumCertKey++;
	return gNumCertKey;
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
	int		len;
	va_list valist;
	
	va_start(valist, format);
	vsnprintf(respBuf,256 * 1024, format,valist);
	len = strlen(respBuf);

	va_end(valist);
	fwrite((unsigned char *)&len,sizeof(len),1,stdout);

	fwrite((unsigned char *)respBuf,len,1,stdout);
	fflush(stdout);
	return len;
}


static int CloseResponse()
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
		if(strcmp(cJc->string,"result") == 0)
		{
			char *testid = cJc->valuestring;
			fprintf(debugParentFP,"result [%s]\n", testid);
			fflush(debugParentFP);
			WaitForChild(1);
			StreamResults(testid);
			exit(0);
		}
		if(strcmp(cJc->string,"targetip") == 0)
		{
			IP = strdup(cJc->valuestring);
		}
		else if(strcmp(cJc->string,"targetport") == 0)
		{
			PORT = cJc->valueint;
		}
		else if(strcmp(cJc->string,"reuse") == 0)
		{
			REUSE = cJc->valueint;
		}
		else if(strcmp(cJc->string,"reneg") == 0)
		{
			RENEG = cJc->valueint;
		}
		else if(strcmp(cJc->string,"cauth") == 0)
		{
			CAUTH = cJc->valueint;
		}
		else if(strcmp(cJc->string,"cipher") == 0)
		{
			CIPHERFILTER = strdup(cJc->valuestring);
		}
		else if(strcmp(cJc->string,"version") == 0)
		{
			VERSIONFILTER = findVerInt(cJc->valuestring);
		}
		else if(strcmp(cJc->string,"reqsize") == 0)
		{
			REQSIZE = atoi(cJc->valuestring);
		}
		else if(strcmp(cJc->string,"recsize") == 0)
		{
			RECSIZE = atoi(cJc->valuestring);
		}
		else if(strcmp(cJc->string,"delay") == 0)
		{
			DELAY = cJc->valueint;
		}
		else if(strcmp(cJc->string,"iter") == 0)
		{
			ITERCOUNT = cJc->valueint;
		}
		else if(strcmp(cJc->string,"recboundary") == 0)
		{
			RECBOUNDARY = cJc->valueint;
		}
		else if(strcmp(cJc->string,"childcount") == 0)
		{
			CHILDCOUNT = cJc->valueint;
			if(CHILDCOUNT > MAXCHILD)
				CHILDCOUNT = MAXCHILD;
		}
		else if(strcmp(cJc->string,"cert") == 0)
		{
			CERTFILE = strdup(cJc->valuestring);
		}
		else if(strcmp(cJc->string,"key") == 0)
		{
			KEYFILE = strdup(cJc->valuestring);
		}
		else if(strcmp(cJc->string,"certlink") == 0)
		{
			CERTLINK = strdup(cJc->valuestring);
		}
		else if(strcmp(cJc->string,"SNI") == 0)
		{
			SERVERNAME = strdup(cJc->valuestring);
		}
		else if(strcmp(cJc->string,"rsapadtest") == 0)
		{
			TESTVAR_rsapadtest = cJc->valueint;
		}
		else if(strcmp(cJc->string,"testid") == 0)
		{
			TESTID_str = strdup(cJc->valuestring);
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
		{
			fprintf(debugParentFP,"killing child %d\n", p->pid);
			fflush(debugParentFP);
			kill(p->pid,9);
		}
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
				*pp = p->next;
				p->next = childStatFreeQ;
				childStatFreeQ = p;
			}
		}
	}
	return 0;
}


int	 CleanChild()
{
	int				count = 0;
	int				status, pid;
	int				found = 0;
	CHILD_STAT_t	**pp, *p;

	while( (pid=wait4(-1,&status,WNOHANG,NULL)) > 0 )
	{
		found = 0;
		for(pp=&childStatActiveQ; p=*pp; pp = &p->next)
		{
			if(p->pid == pid)	
			{
				*pp = p->next;
				p->next = childStatFreeQ;
				childStatFreeQ = p;
				count++;
				found = 1;
			}
		}
		if(!found)
			fprintf(debugParentFP,"no child for %d\n", pid);
	}
	return count;
}




static int	findVerInt(char *v)
{
	int	i;
	for(i=0;vers[i];i++)
	{
		if(strcmp(vers[i],v) == 0)
			return verInt[i];
	}
	return -1;
}


int	FillCommonNames(X509 *x509, char *out)
{
	const X509V3_EXT_METHOD		*meth;
	X509_EXTENSION			*ext;
	STACK_OF(X509_EXTENSION) *exts;
	STACK_OF(CONF_VALUE) 	*nval = NULL;
	X509_NAME				*subjname;
	const unsigned char		*p;
	int						i;
	void					*ext_str = NULL;
	char					*ptr = out;

	if(!x509)
	{
		strcpy(out,"None");
		return 0;
	}

	exts = x509->cert_info->extensions;

	subjname = x509->cert_info->subject;
	for(i=0; i<sk_X509_NAME_ENTRY_num(subjname->entries); i++)
	{
		X509_NAME_ENTRY *e;
		e = sk_X509_NAME_ENTRY_value(subjname->entries,i);
		if(NID_commonName == OBJ_obj2nid(e->object))
		{
			ptr += sprintf(ptr,"%s ", e->value->data);
		}
	}

	for (i=0; i<sk_X509_EXTENSION_num(exts); i++)
	{
		ext = sk_X509_EXTENSION_value(exts, i);
		if(NID_subject_alt_name == OBJ_obj2nid(ext->object))
		{
			meth = X509V3_EXT_get(ext);
			p = ext->value->data;

		 	if(meth->it)
				ext_str = ASN1_item_d2i(NULL, &p, ext->value->length,
												ASN1_ITEM_ptr(meth->it));
			else
				ext_str = meth->d2i(NULL, &p, ext->value->length);

			nval = meth->i2v(meth,ext_str,NULL);
			for(i=0; i<sk_CONF_VALUE_num(nval); i++)
			{
				CONF_VALUE *cval;
				cval = sk_CONF_VALUE_value(nval,i);
				ptr += sprintf(ptr,"%s ", cval->value);
			}
			break;
		}
	}

	return 0;
}



int	StreamFileByLine(char *file)
{
	FILE	*fp = fopen(file,"r");
	char	buf[1024];
	int		count=0;

	if(!fp)
		return -1;

	while(fgets(buf,1023,fp))
	{
		WriteResponse("%s\n",buf);
		count++;
		if(count%16 == 0)
			usleep(1024 * 100);
	}
	fclose(fp);
	return count;	
}


int	StreamResults(char *testid)
{
	int				len = 0,count  = 0;
	char			filename[128];


	for(count=0; count < MAXCHILD; count++)
	{
		sprintf(filename,"/tmp/debug.client.%s.%d",testid,count);
		fprintf(debugParentFP,"Streaming %s\n",filename);
		len += StreamFileByLine(filename);
	}

	WriteResponse("%s","");
	return len;
}
