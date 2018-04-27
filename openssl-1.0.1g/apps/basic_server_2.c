#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
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
#include "openssl/ssl.h"
#include <openssl/dh.h>
#include <openssl/ec.h>
#include <openssl/bio.h>
#include <openssl/err.h>
#include <sys/select.h>
#include "cJSON.h"


const SSL_METHOD        *v30Method = NULL;
const SSL_METHOD        *v31Method = NULL;
const SSL_METHOD        *v32Method = NULL;
const SSL_METHOD        *v33Method = NULL;


typedef struct _child_stat_ {
	int							id;
	int 						pid;
	int							pass;
	int							fail;
	X509						*childServerCert;
	EVP_PKEY 					*childServerKey;
	char						*childSendCAFile;
	char						*childVerifyCAFile;
	DH							*childDH;
	EC_KEY						*childECDH;
	const SSL_METHOD			*childMethod;
	const SSL_CIPHER			*childCipher;
	struct 		_child_stat_	*next;	
	char						childLogFile[128];
	char						sessFile[128];
} CHILD_STAT_t;


typedef struct _cert_list_ {
	X509		*s_cert;
	EVP_PKEY	*s_key;
	char		*sigalg;
	int			keysize;
} CERT_LIST_t;

typedef struct _dh_list_ {
	DH	*dh;
} DH_LIST_t;

const SSL_METHOD		*MethodList[4];
EC_KEY					*ECKeyList[4];

#if 0
char					*ECCurveNameList[4] = {"secp256k1","secp384r1",
												"secp224r1","secp521r1"};
#endif

char					*ECCurveNameList[4] = {"prime256v1","secp384r1",
												"secp224r1","secp521r1"};




SSL_CTX 				*newCTX();
int						loadCerts();
int 					initSocket(char *ip, int port);
int						ProcessChildStat(CHILD_STAT_t *stat, int status);
EC_KEY					*getNextECDH(int reset);
DH						*getNextDH(int reset);
const SSL_METHOD		*getNextMethod(int reset);
const SSL_CIPHER		*getNextCipher(const SSL_METHOD *meth,int reset);
int						getNextCertKey(X509 **certpp,EVP_PKEY **keypp,int reset);
int						ResetState();
static 	DH 				*load_dh_param(const char *dhfile);
int						doResponseHandshakeDetails(SSL *s);
int						FailMessage();
int						CipherFilter(unsigned int version,const SSL_CIPHER *c);
static int				readCmdData(int fd,unsigned char *buf,int *len);
static int				WriteResponse(char *format, ...);
int     				CloseResponse();
char 					*Create1MBRespData();
int						doResponseBySize(SSL *s);
int  					WaitForChild(int kill);
int	 					CleanChild();
int						StreamFileByLine(char *file);
int						StreamResults();
SSL_SESSION 			*GetSessionCB(SSL *,unsigned char *,int ,int *);
static int				HandleArgs(char * buf);
static int 				SendResult(SSL *ssl,char *status);
static int 				SendEmptyResult(int ,const char *);
static int 				Delay(int i);

static int				ResponseProfileOne(SSL *s);
static int				ResponseProfileTwo(SSL *s);


extern	X509 			*ssl_get_server_send_cert(const SSL *s);
extern	DH      		*SSL_get_dh(SSL *s);
extern	char    		*SSL_get_curvename(SSL *s);
extern  char			*ASHOKE_TOOL_get_cert_info(X509 *,char *);
extern  char			*ASHOKE_TOOL_get_ecc_info(SSL *);
extern	int				ASHOKE_TOOL_write_session(SSL *, char *);
extern	SSL_SESSION		*ASHOKE_TOOL_find_session(unsigned char *, char *);

CERT_LIST_t				gCertList[1024];
int						gNumCertKey = 0;

DH						*gDHList[64];
int						gNumDH = 0;


CHILD_STAT_t 			*curChildStat = NULL;
CHILD_STAT_t			*childStatFreeQ = NULL;
CHILD_STAT_t			*childStatActiveQ = NULL;
char					*CIPHERFILTER = NULL;

char					*IP = NULL;
int						PORT = 0;
int						REUSE = 0;
int						RENEG = 0;
int						CAUTH = 0;
int						RESPSIZE = 0;
int						RESPPROFILE = 0;
int						RECORDSIZE = 0;
int						DELAY = 0;


#define			MAXCHILD		4

#define			SSL_SSLV2		0x00000001L
#define			SSL_SSLV3		0x00000002L
#define			SSL_TLSV1		SSL_SSLV3 
#define			SSL_TLSV1_2		0x00000004L

#define			SSL_kEDH		0x00000008L
#define			SSL_kEECDH		0x00000080L


char			*ECCURVES[] = { "secp256r1",
								"secp256r1",
								"secp224r1",
								"secp521r1" };

char			*glbRespBuf = NULL;
char			*glbRespCurPtr = NULL;
int				glbRespLen = 0;
FILE			*debugParentFP = NULL;
FILE			*debugChildFP = NULL;


#define		printf		WriteResponse
extern char data_16384[];

int main(int argc, char **argv)
{
	int						asd, sd;
	int						len, childCount=0;
	int						i,pid = -1;
	int						status = 0, ret;
	int						curCert,curDH,curMethod,curCiphIdx;
	char					namebuf[256];
	char					sessdbfile[256];
	unsigned char			buf[1024];
	const SSL_METHOD		*meth;
	const SSL_CIPHER		*cipher;
	DH						*dh;
	EC_KEY					*ecKey;
	X509					*cert;
	EVP_PKEY				*pkey;
	CHILD_STAT_t			*tChildStat;
	struct	sockaddr_in		from;
	FILE					*fp;
	fd_set					readfds;
	struct	timeval			tv;
	volatile int			mydebug = 1;

	chdir("/tmp");
	sprintf(namebuf,"debug.parent.%d.log",getpid());
	debugParentFP = fopen(namebuf,"w");
	setbuf(debugParentFP,NULL);

	chdir("/mnt/ToolPkg/Server");
	glbRespBuf = Create1MBRespData();
	glbRespCurPtr = glbRespBuf;


	len =  sizeof(buf) - 1;
	ret = readCmdData(0, buf, &len);
	if(ret <= 0)
		return 0;

	if(strcmp(buf,"twinkletwinkle"))
		return 0;
	WriteResponse("%s","howiwonder");

	len =  sizeof(buf) - 1;
	ret = readCmdData(0, buf, &len);
	if(ret <= 0)
		return ret;

	HandleArgs(buf);

	asd = initSocket(IP,PORT);
	listen(asd,5);

	sprintf(sessdbfile,"/tmp/session.%d.db",getpid());
	fp = fopen(sessdbfile,"w");
	fclose(fp);

	for(ret=0; ret < MAXCHILD ; ret++)
	{
		tChildStat = (CHILD_STAT_t *)malloc(sizeof(CHILD_STAT_t));
		tChildStat->pid = 0;
		tChildStat->id = 0;
		sprintf(tChildStat->childLogFile,"/tmp/debug.child.%d.%d",getpid(),ret);
		tChildStat->next = childStatFreeQ;
		childStatFreeQ = tChildStat;

		debugChildFP = fopen(tChildStat->childLogFile,"w");
		fclose(debugChildFP);
		debugChildFP = NULL;

		strcpy(tChildStat->sessFile,sessdbfile);
	}

	SSL_load_error_strings();

	if(loadCerts() <= 0)
	{
		fprintf(debugParentFP,"Failed to load even a single cert..\n");
		exit(0);
	}

	if(loadDHs() <= 0)
	{
		fprintf(debugParentFP,"Failed to load even a single DH..\n");
		exit(0);
	}

	MethodList[0]       = SSLv3_server_method();
	MethodList[1]       = TLSv1_server_method();
	MethodList[2]       = TLSv1_1_server_method();
	MethodList[3]       = TLSv1_2_server_method();

	for(i=0; i<sizeof(ECCurveNameList)/sizeof(ECCurveNameList[0]); i++)
	{
		ECKeyList[i] = EC_KEY_new_by_curve_name(OBJ_sn2nid(ECCurveNameList[i]));
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
				fprintf(debugParentFP,"Parent:: exiting after cleaning child.\n");
				WaitForChild(1);
				return 0;
			}

			HandleArgs(buf);
		}

		if(!FD_ISSET(asd,&readfds))
			continue;

		len = sizeof(from);

		childCount = 0;
		meth = NULL;
		cipher = NULL;
		dh = NULL;
		ecKey = NULL;
		cert = NULL;
		pkey = NULL;


RESET:

		while((meth = getNextMethod(0)))
		{
		while((cipher = getNextCipher(meth,0)))
		{
			if(!CipherFilter(meth->version,cipher))
				continue;
		while(getNextCertKey(&cert,&pkey,0))
		{
			do
			{

			if(cipher->algorithm_mkey & SSL_kEDH)
			{
				dh = getNextDH(0);
				if(!dh)
					continue;
				ecKey = NULL;
			}
			else if(cipher->algorithm_mkey & SSL_kEECDH)
			{
				ecKey = getNextECDH(0);
				if(!ecKey)
					continue;
				dh = NULL;
			}

			while(!childStatFreeQ)
			{
				//WriteResponse("Waiting for childStatFreeQ");
				sleep(1);
				childCount -= CleanChild();
			}


			while(1)
			{
				FD_ZERO(&readfds);
				FD_SET(asd,&readfds);
				FD_SET(0,&readfds);
				select(asd+1,&readfds,NULL,NULL,&tv);
				childCount -= CleanChild();

				if(FD_ISSET(0,&readfds))
				{
					len =  sizeof(buf) - 1;
					ret = readCmdData(0, buf, &len);
					if((ret <= 0) || (len == 0))
					{
						WaitForChild(1);
						return 0;
					}
					HandleArgs(buf);
					ResetState();
					goto RESET;
				}

				if(FD_ISSET(asd,&readfds))
				{
					break;
				}
			}

			listen(asd,5);
			sd = accept(asd,(struct sockaddr *)&from,(void *)&len);
			if(sd <= 0)
			{
				fprintf(debugParentFP,"main() accept failed..\n");
				fflush(debugParentFP);
				perror("accept::");
				exit(0);
			}

			curChildStat		= childStatFreeQ;
			childStatFreeQ		= childStatFreeQ->next;
			curChildStat->next	= childStatActiveQ;
			childStatActiveQ	= curChildStat;
			curChildStat->pass  = curChildStat->fail = curChildStat->pid = 0;

			curChildStat->childMethod		= meth;
			curChildStat->childCipher		= cipher;
			curChildStat->childServerCert	= cert;
			curChildStat->childServerKey	= pkey;
			curChildStat->childSendCAFile	= "server_ca_file";
			curChildStat->childVerifyCAFile = "server_ca_file";
			curChildStat->childDH			= dh;
			curChildStat->childECDH			= ecKey;
			curChildStat->id++;


			pid = fork();
			if(pid > 0)
			{
				CHILD_STAT_t	*p, **pp;

				close(sd);
				curChildStat->pid = pid;
				childCount++;

				while( (pid=wait4(-1,&status,WNOHANG,NULL)) > 0 )
				{
					childCount--;
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

				if(childCount > MAXCHILD)
				{
					ret = wait4(-1,&status,0,NULL);
					if(ret > 0)
						childCount--;
				}
				continue;
			}
			else if (pid == 0)
			{
				debugChildFP = fopen(curChildStat->childLogFile,"a");
				setbuf(debugChildFP,NULL);

				ret = doChild(sd);

				if(debugChildFP)
				{
					fclose(debugChildFP);
					debugChildFP = NULL;
				}
				close(sd);
				exit(ret);
			}

			childCount -= CleanChild();
			} while(dh ||  ecKey);
		}
		}
		}

		if(glbRespCurPtr !=  glbRespBuf)
		{
			*glbRespCurPtr = 0;
			WriteResponse("%s",glbRespBuf);
			glbRespCurPtr = glbRespBuf;
		}
	
	}
}




int	doChild(int sd)
{
	SSL_CTX	*ctx;
	BIO		*sbio, *ssl_bio;
	SSL		*con;
	char	buf[1024];
	char	obuf[1024];
	int		ret = 0;
	volatile int		childDebug = 1;


	chdir("/tmp");
	ctx = newCTX();
	if(!ctx)
		return -1;

	sbio=BIO_new_socket(sd,BIO_NOCLOSE);
	if(!sbio)
		return -2;

	ssl_bio=BIO_new(BIO_f_ssl());
	if(!ssl_bio)
		return -3;

	con = SSL_new(ctx);
	if(!con)
		return -4;

	SSL_set_bio(con,sbio,sbio);
	SSL_set_accept_state(con);
	BIO_set_ssl(ssl_bio,con,BIO_CLOSE);

	if(REUSE)
		SSL_set_reuse_count(con,5);
	else
		SSL_set_reuse_count(con,0);

	ret = SSL_accept(con);

	if(con->first_packet)
		return -5;

	if(ret <= 0)
	{
		unsigned long l;
		char	*ptr;

		struct	sockaddr_in peer;
		int		peerlen = sizeof(peer);
		
		l=ERR_get_error();
		ptr = ERR_error_string(l,NULL);

		SendResult(con,ptr);

		return -5;
	}

	ASHOKE_TOOL_write_session(con,curChildStat->sessFile);

	ret = SSL_read(con,buf,sizeof(buf)-1);
	if(ret <= 0)
	{
		unsigned long l;
		char	*ptr;
		struct	sockaddr_in peer;
		int		peerlen = sizeof(peer);

		l=ERR_get_error();
		ptr = ERR_error_string(l,NULL);
		SendResult(con,ptr);
		return -6;
	}

	if(RESPPROFILE == 0)
		ResponseProfileOne(con);
	if(RESPPROFILE == 1)
		ResponseProfileTwo(con);

	SendResult(con,"Success");

	SSL_shutdown(con);
	return 0;
}





SSL_CTX *newCTX()
{
	SSL_CTX				*ctx;
	DH					*dh;
	int					certId;
	struct 				timeval tv;

	SSL_load_error_strings();
	SSL_library_init();

	ctx = SSL_CTX_new(curChildStat->childMethod);

	SSL_CTX_set_options(ctx,SSL_OP_ALL);
	SSL_CTX_sess_set_cache_size(ctx,128);

	SSL_CTX_use_certificate(ctx,curChildStat->childServerCert);
	SSL_CTX_use_PrivateKey(ctx,curChildStat->childServerKey);


	if(curChildStat->childDH)
		SSL_CTX_set_tmp_dh(ctx,curChildStat->childDH);
	if(curChildStat->childECDH)
		SSL_CTX_set_tmp_ecdh(ctx,curChildStat->childECDH);


	SSL_CTX_load_verify_locations(ctx,curChildStat->childVerifyCAFile,NULL);
	SSL_CTX_set_client_CA_list(ctx,SSL_load_client_CA_file(curChildStat->childSendCAFile));
	if(CAUTH)
		SSL_CTX_set_verify(ctx,SSL_VERIFY_PEER|SSL_VERIFY_FAIL_IF_NO_PEER_CERT|SSL_VERIFY_CLIENT_ONCE, NULL);


	if(curChildStat->childCipher)
	{
		if(!SSL_CTX_set_cipher_list(ctx,curChildStat->childCipher->name))
		{
			SendEmptyResult(0,curChildStat->childCipher->name);
			return NULL;
		}
	}

	SSL_CTX_sess_set_get_cb(ctx,GetSessionCB);

	gettimeofday(&tv,NULL);
	srandom(tv.tv_usec);
	certId = random() % gNumCertKey;
	

	return ctx;
}



int	loadCerts()
{
	char	certName[64];
	char	keyName[64];
	int		i,j,k, x;

	int		serverbits[] = {1024,2048,4096};
	int		sigbits[]    = {1,256,384};
	int		dhbits[]     = {1024,2048};

	struct	stat sb;
	BIO		*cert;
	BIO		*key;

	for(x = 0; x < sizeof(gCertList)/sizeof(gCertList[0]); x++)
	{
		gCertList[x].s_cert = NULL;
		gCertList[x].s_key  = NULL;
	}

	for(i=0; i < sizeof(serverbits)/sizeof(serverbits[0]); i++)
	for(j=0; j < sizeof(sigbits)/sizeof(sigbits[0]); j++)
	{
		bzero(certName,sizeof(certName));
		bzero(keyName,sizeof(keyName));

		sprintf(certName,"Server%d_sha%d_cert.pem",
										serverbits[i],sigbits[j]);
		sprintf(keyName,"Server%d_sha%d_key.pem",
										serverbits[i],sigbits[j]);

		if((stat(certName,&sb)==-1) || (stat(keyName,&sb)==-1))
			break;

		if ((cert=BIO_new(BIO_s_file())) == NULL)
			continue;
		if ((key=BIO_new(BIO_s_file())) == NULL)
		{
			BIO_free(cert);
			continue;
		}

		if (BIO_read_filename(cert,certName) <= 0)
		{
			BIO_free(cert);
			continue;
		}
		if (BIO_read_filename(key,keyName) <= 0)
		{
			BIO_free(cert);
			BIO_free(key);
			continue;
		}

		if( !(gCertList[gNumCertKey].s_cert = 
			PEM_read_bio_X509_AUX(cert,NULL,NULL,NULL)) )
		{
			BIO_free(cert);
			BIO_free(key);
			continue;
		}

		if( !(gCertList[gNumCertKey].s_key = 
			PEM_read_bio_PrivateKey(key,NULL,NULL,NULL)) )
		{
			X509_free(gCertList[gNumCertKey].s_cert);
			BIO_free(cert);
			BIO_free(key);
			continue;
		}

		{
		EVP_PKEY *pktmp = X509_get_pubkey(gCertList[gNumCertKey].s_cert);
		BIO *bp = BIO_new(BIO_s_mem());
		gCertList[gNumCertKey].keysize = EVP_PKEY_bits(pktmp);
		EVP_PKEY_free(pktmp);
		gCertList[gNumCertKey].sigalg = malloc(32);
		X509_signature_print(bp,gCertList[gNumCertKey].s_cert->sig_alg,NULL);
		BIO_gets(bp,gCertList[gNumCertKey].sigalg,31);
		if(gCertList[gNumCertKey].sigalg[strlen(gCertList[gNumCertKey].sigalg)-1] == '\n')
			gCertList[gNumCertKey].sigalg[strlen(gCertList[gNumCertKey].sigalg)-1] = 0;	
		BIO_free(bp);
		}

		BIO_free(cert);
		BIO_free(key);

		gNumCertKey++;
	}
	return gNumCertKey;
}


int	loadDHs()
{
	int		x;

	for(x = 0; x < sizeof(gDHList)/sizeof(gDHList[0]); x++)
	{
		gDHList[x] = NULL;
	}

	gDHList[0] = load_dh_param("dh_1024");
	gNumDH++;
	gDHList[1] = load_dh_param("dh_2048");
	gNumDH++;

	return gNumDH;
}


static DH *load_dh_param(const char *dhfile)
{
	DH *ret=NULL;
	BIO *bio;

	if ((bio=BIO_new_file(dhfile,"r")) == NULL)
		goto err;
	ret=PEM_read_bio_DHparams(bio,NULL,NULL,NULL);
err:
	if (bio != NULL) BIO_free(bio);
	return(ret);
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
	setsockopt(s,SOL_SOCKET,SO_RCVTIMEO,&tv,sizeof(tv));

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
	int		ver = 0;
	int		certbit = 0;
	int		clntcertbit = 0;
	int		dhbit = 0;
	int		reuse = 0;
	int		reneg = 0;
	int		x;
	const char	*ciphername = NULL;
	char	*curvename = NULL;
	char	*sigalg = NULL;
	char	*pass = NULL;
	char	respBuf[2048];

	if(status)
		pass = "Fail";
	else
		pass = "Pass";

	/********************************************************
		ver | cipher | cert bit | cert sigalg | dh bit | curvename | reuse | reneg | clnt cert bit | pass/fail 
		%d | %s | %d | %s | %d | %s | %d | %d | %d | %d
	 *******************************************************/
	
	ver = stat->childMethod->version;
	ciphername = stat->childCipher->name;
	
	for(x=0; x<gNumCertKey; x++)
	{
		if(gCertList[x].s_cert == stat->childServerCert)
		{
			certbit = gCertList[x].keysize;
			sigalg = gCertList[x].sigalg;
		}
	}

	if(stat->childECDH)
	{
	for(x=0; x<sizeof(ECKeyList)/sizeof(ECKeyList[0]); x++)
	{
		if(ECKeyList[x] == stat->childECDH)	
		{
			curvename = ECCurveNameList[x];
			break;
		}
	}
	}

	if(stat->childDH)
		dhbit = BN_num_bits(stat->childDH->p);

	
	glbRespCurPtr += sprintf(glbRespCurPtr,"%02x %30s %04d %26s %04d %12s %d %d %04d %d\n", ver,ciphername,certbit,sigalg,dhbit,curvename,reuse,reneg, clntcertbit,status);
	if((glbRespCurPtr - glbRespBuf) >= 8192)
	{
		*glbRespCurPtr = 0;
		WriteResponse("%s",glbRespBuf);
		glbRespCurPtr = glbRespBuf;
	}


	return 0;
}


EC_KEY	*getNextECDH(int reset)
{
	static int nextKey = 0;
	EC_KEY	*key = NULL;

	if(reset)
	{
		nextKey = 0;
		return NULL;
	}
	
	if(nextKey >= (sizeof(ECKeyList)/sizeof(ECKeyList[0])) )
	{
		nextKey = 0;
		return NULL; //indicates  end of an iteration
	}

	key = ECKeyList[nextKey++];

	return key;
}


DH	*getNextDH(int reset)
{
	static int nextDH = 0;
	DH	*dh;

	if(reset)
	{
		nextDH = 0;
		return NULL;
	}

	if(nextDH >= gNumDH) 
	{
		nextDH = 0;
		return NULL;
	}

	dh = gDHList[nextDH++];
	return dh;
}


const SSL_METHOD	*getNextMethod(int reset)
{
	static int nextMethod = 0;
	const SSL_METHOD	*meth;

	if(reset)
	{
		nextMethod = 0;
		return NULL;
	}

	if(nextMethod >= (sizeof(MethodList)/sizeof(MethodList[0])) )
	{
		nextMethod = 0;
		return NULL;
	}
	meth = MethodList[nextMethod++];
	return meth;
}


int		getNextCertKey(X509 **certpp, EVP_PKEY **keypp,int reset)
{
	static int nextCertKey = 0;

	if(reset)
	{
		nextCertKey = 0;
		return 0;
	}

	if(nextCertKey >= gNumCertKey)
	{
		nextCertKey = 0;
		return 0;
	}
	
	*certpp = gCertList[nextCertKey].s_cert;
	*keypp  = gCertList[nextCertKey].s_key;
	nextCertKey++;
	
	return 1;
}


const SSL_CIPHER	*getNextCipher(const SSL_METHOD *meth,int reset)
{
	static int m0Idx = 0;
	static int m1Idx = 0;
	static int m2Idx = 0;
	static int m3Idx = 0;
	int					*idxp = NULL;
	const SSL_CIPHER	*cipher = NULL;

	if(reset)
	{
		m0Idx = m1Idx = m2Idx = m3Idx = 0;
		return NULL;
	}

	if(meth == MethodList[0])
		idxp = &m0Idx;
	else if(meth == MethodList[1])
		idxp = &m1Idx;
	if(meth == MethodList[2])
		idxp = &m2Idx;
	else if(meth == MethodList[3])
		idxp = &m3Idx;


	if(*idxp >= meth->num_ciphers())
	{
		*idxp = 0;
		return NULL;
	}

CONT :
	cipher = meth->get_cipher(*idxp);
	(*idxp)++;

	if(!cipher->valid)
		goto CONT;

	if(*idxp >= meth->num_ciphers())
	{
		*idxp = 0;
		return NULL;
	}

	if( (meth->version == 0x0300) && 
		(cipher->algorithm_ssl > SSL_SSLV3) )
			goto CONT;

	if( (meth->version == 0x0301) && 
		(cipher->algorithm_ssl > SSL_TLSV1) )
			goto CONT;

	if( (meth->version == 0x0302) && 
		(cipher->algorithm_ssl > SSL_TLSV1) )
			goto CONT;

	if( (meth->version == 0x0303) && 
		(cipher->algorithm_ssl > SSL_TLSV1_2) )
			goto CONT;
	
	return cipher;
}

int		ResetState()
{
	getNextECDH(1);
	getNextDH(1);
	getNextMethod(1);
	getNextCertKey(NULL,NULL,1);
	getNextCipher(NULL,1);
	return 0;
}


int		FailMessage()
{
	EVP_PKEY	*pktmp;
	BIO			*bp;
	X509		*x = curChildStat->childServerCert;
	char		tbuf[256];
	char		fbuf[8192];
	char		*ptr = fbuf;

	ptr += sprintf(ptr,"Error Case :\n");
	ptr += sprintf(ptr,"------------\n");
	ptr += sprintf(ptr,"Version : %x\n", curChildStat->childMethod->version);
	ptr += sprintf(ptr,"Cipher  : %s\n", curChildStat->childCipher->name);
	ptr += sprintf(ptr,"Subject : %s\n", X509_NAME_oneline(x->cert_info->subject,NULL,0) );

	pktmp = X509_get_pubkey(x);
	ptr += sprintf(ptr,"Server Cert : %d  ",EVP_PKEY_bits(pktmp));
	EVP_PKEY_free(pktmp);

	bp = BIO_new(BIO_s_mem());
	X509_signature_print(bp,x->sig_alg,NULL);
	BIO_gets(bp,tbuf,sizeof(tbuf)-1);
	ptr += sprintf(ptr,"%s", tbuf);
	ptr += sprintf(ptr,"\n");
	BIO_flush(bp);

	if(curChildStat->childDH)
		ptr += sprintf(ptr,"DH : %d\n", BN_num_bits(curChildStat->childDH->p));

	if(curChildStat->childECDH)
		ptr += sprintf(ptr,"ECC : %s\n", SSL_get_curvename2(curChildStat->childECDH));

	return 0;
}



int	doResponseBySize(SSL *s)
{
	int		len,iter,recsize,rem,ret;
	char	*ptr = glbRespBuf;

	len = sprintf(glbRespBuf,"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: %d\r\n\r\n", RESPSIZE);
	glbRespBuf[len] = 'X';

	iter = RESPSIZE / RECORDSIZE;
	rem  = RESPSIZE % RECORDSIZE;

	while(iter)
	{
		recsize = RECORDSIZE;

		while(recsize)
		{
			ret = SSL_write(s,ptr,RECORDSIZE);
			if(ret <= 0)
				break;
			ptr += ret;
			recsize -= ret;
		}
		if(ret <= 0)
			break;
		
		iter--;
	}
	
	if((ret > 0) && rem)
	{
		recsize = rem;
		while(recsize)
		{
			ret = SSL_write(s,ptr,RECORDSIZE);
			if(ret <= 0)
				break;
			ptr += ret;
			recsize -= ret;
		}
	}
	SSL_shutdown(s);
	return 0;
}




int		doResponseHandshakeDetails(SSL *s)
{
	char	*buf;
	char	*ptr;
	char	*ecname;
	char	tbuf[128];
	int		ret,len;
	DH		*dh;
	X509	*x;

	buf = malloc(16 * 1024);
	ptr = buf;
	
	ptr += sprintf(ptr,"Version : %x\n", SSL_version(s));
	ptr += sprintf(ptr,"Cipher  : %s\n", SSL_get_current_cipher_name(s));

#if 0
	if(x = ssl_get_server_send_cert(s))
	{
		EVP_PKEY	*pktmp;
		BIO			*bp;

		ptr += sprintf(ptr,"Subject : %s\n", 
			X509_NAME_oneline(x->cert_info->subject,NULL,0) );
		ptr += sprintf(ptr,"Issuer : %s\n", 
			X509_NAME_oneline(x->cert_info->issuer,NULL,0));

		pktmp = X509_get_pubkey(x);
		ptr += sprintf(ptr,"Server Cert : %d  ",EVP_PKEY_bits(pktmp));
		EVP_PKEY_free(pktmp);

		bp = BIO_new(BIO_s_mem());
		X509_signature_print(bp,x->sig_alg,NULL);
		BIO_gets(bp,tbuf,sizeof(tbuf)-1);
		ptr += sprintf(ptr,"%s", tbuf);
		BIO_flush(bp);
		BIO_free(bp);	
	}
#endif


	ASHOKE_TOOL_get_cert_info(ssl_get_server_send_cert(s),tbuf);
	ptr += sprintf(ptr,"ServerCert: %s\n",tbuf); 

	tbuf[0] = 0;
	if(s->session->peer)
		ASHOKE_TOOL_get_cert_info(s->session->peer,tbuf);
	else
		strcpy(tbuf,"None");
	ptr += sprintf(ptr,"ClientCert: %s\n",tbuf); 

	if((dh=SSL_get_dh(s)))
	{
	ptr += sprintf(ptr,"DH : %d\n", BN_num_bits(dh->p));
	}
	if((ecname=SSL_get_curvename(s)))
	{
		ptr += sprintf(ptr, "ECC : %s\n", ecname);
	}
	*ptr = 0;


	sprintf(tbuf,"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: %d\r\n\r\n", strlen(buf));
	len = strlen(tbuf);
	ptr = tbuf;


	while(len)
	{
		ret = SSL_write(s,ptr,len);
		if(ret <= 0)
			break;
		len -= ret;
		ptr += ret;
	}

	fprintf(debugChildFP,"%s\n",buf);
	fclose(debugChildFP);
	debugChildFP = NULL;
	len = strlen(buf);
	ptr = buf;
	while(len)
	{
		ret = SSL_write(s,ptr,len);
		if(ret <= 0)
			break;
		len -= ret;
		ptr += ret;
	}
	SSL_shutdown(s);
	free(buf);
	return 0;
}


int		CipherFilter(unsigned int version,const SSL_CIPHER *c)
{
	char	*excludefilerStr[] = {"NULL","ECDSA","DSS","EXP-","EXP1024","ADH-AES128-GCM-SHA256", "ADH-AES256-GCM-SHA384"};
	int		excludefilterCount = 
			sizeof(excludefilerStr)/sizeof(excludefilerStr[0]);
	int		i;

	for(i=0; i<excludefilterCount; i++)
		if(strstr(c->name,excludefilerStr[i]))
			return 0;

	if(version == 0x0303)
	{
		char *excludeFilter[] = {"ADH-", "DES-CBC-"};
		int	 excludeFilterCount = 
			sizeof(excludeFilter)/sizeof(excludeFilter[0]);
		int	i;
		for(i=0; i<excludeFilterCount; i++)
			if(strstr(c->name,excludeFilter[i]))
				return 0;
	}


	if(CIPHERFILTER && strlen(CIPHERFILTER) && !strstr(c->name,CIPHERFILTER))
	{
		return 0;
	}
	return 1;
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

volatile int mydebug=1;

	fprintf(debugParentFP,"HandleArgs : [%s]\n", buf);
	fflush(debugParentFP);

	if(buf[0] == '[')
		bcopy(buf+1,buf,strlen(buf)-1);

	cJ  = cJSON_Parse(buf);
	if(!cJ)
	{
		fprintf(debugParentFP,"cJSON_Parse failed\n");
		fflush(debugParentFP);

		WriteResponse("cJSON_Parse failed\n");
		fflush(stderr);
		exit(0);
	}

	cJc = cJ->child;
	while(cJc)
	{
		if(strcmp(cJc->string,"result") == 0)
		{
			fprintf(debugParentFP,"results :: waiting for child\n");
			fflush(debugParentFP);

			WaitForChild(0);
			fprintf(debugParentFP,"results :: waiting for child over\n");
			fflush(debugParentFP);
			StreamResults();
		}
		else if(strcmp(cJc->string,"listen_port") == 0)
		{
			PORT = atoi(cJc->valuestring);
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
		else if(strcmp(cJc->string,"cipher_filter") == 0)
		{
			CIPHERFILTER = strdup(cJc->valuestring);
		}
		else if(strcmp(cJc->string,"resp_profile") == 0)
		{
			RESPPROFILE = cJc->valueint;
		}
		else if(strcmp(cJc->string,"record_size") == 0)
		{
			RECORDSIZE = cJc->valueint;
		}
		else if(strcmp(cJc->string,"resp_size") == 0)
		{
			RESPSIZE = cJc->valueint;
		}
		else if(strcmp(cJc->string,"inter_record_delay") == 0)
		{
			DELAY = cJc->valueint;
		}
		cJc = cJc->next;
	}
	return 0;
}



char *Create1MBRespData()
{
	char Alpha[] = {'0','1','2','3','4','5','6','7',
					'8','9','A','B','C','D','E','F' };
	char	*Resp1MB = malloc(1024 * 1024);
	char	*ptr = Resp1MB;
	int		iter = (1024 * 1024)/sizeof(Alpha);
	int		i;

	if(!Resp1MB)
		return NULL;

	for(i=0; i<iter; i++)
	{
		bcopy(Alpha,ptr,sizeof(Alpha));
		ptr += sizeof(Alpha);
	}
	return Resp1MB;
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


static int SendResult(SSL *ssl,char *status)
{
	cJSON	*root, *cJ,*cjArray;
	DH		*dh;
	char	*ecname,*out = NULL;
	char	buf[1024];
	char	tbuf[1024];
	int		i;

	root	= cJSON_CreateObject();

	sprintf(buf,"0x%x",SSL_version(ssl));
	cJSON_AddStringToObject(root,"version", buf);

	if(ssl->session && ssl->session->cipher)
		cJSON_AddStringToObject(root,"cipher",SSL_get_current_cipher_name(ssl));
	else
		cJSON_AddStringToObject(root,"cipher", curChildStat->childCipher->name);

	tbuf[0] = 0;
	if(ssl->s3->tmp.new_cipher)
		ASHOKE_TOOL_get_cert_info(ssl_get_server_send_cert(ssl),tbuf);
	else
		strcpy(tbuf,"Unknown");
		
	cJSON_AddStringToObject(root,"ServerCert", tbuf);


	tbuf[0] = 0;
	if(ssl->session && ssl->session->peer && ssl->session->peer)
		ASHOKE_TOOL_get_cert_info(ssl->session->peer,tbuf);
	else
		strcpy(tbuf,"None");
	cJSON_AddStringToObject(root,"ClientCert", tbuf);

	if((dh=SSL_get_dh(ssl)))
	{
		sprintf(tbuf,"%d", BN_num_bits(dh->p));
	}
	else
		strcpy(tbuf,"None");
	cJSON_AddStringToObject(root,"DH", tbuf);

	if((ecname=SSL_get_curvename(ssl)))
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

	cJSON_AddNumberToObject(root,"a", curChildStat->id);


	cJSON_AddStringToObject(root,"result", status);

	cjArray = cJSON_CreateArray();
	cJSON_AddItemToArray(cjArray,root);
	out	=	cJSON_PrintUnformatted(root);
	fprintf(debugChildFP,"%s\n",out);
	fflush(debugChildFP);
	cJSON_Delete(cjArray);
	return 0;
}


static int SendEmptyResult(int version,const char *cipher)
{
	cJSON	*root, *cJ,*cjArray;
	char	buf[1024], *out;

	root	= cJSON_CreateObject();

	sprintf(buf,"0x%x",version);
	cJSON_AddStringToObject(root,"version", buf);
	cJSON_AddStringToObject(root,"cipher", cipher);
	cJSON_AddStringToObject(root,"ServerCert", " ");
	cJSON_AddStringToObject(root,"ClientCert", " ");
	cJSON_AddStringToObject(root,"DH", " ");
	cJSON_AddStringToObject(root,"ECC", " ");
	cJSON_AddNumberToObject(root,"reuse", 0);
	cJSON_AddNumberToObject(root,"reneg", 0);
	cJSON_AddStringToObject(root,"result", "Failure");
	cJSON_AddNumberToObject(root,"a", curChildStat->id);

	cjArray = cJSON_CreateArray();
	cJSON_AddItemToArray(cjArray,root);
	out	=	cJSON_PrintUnformatted(root);
	fprintf(debugChildFP,"%s\n",out);
	fflush(debugChildFP);
	cJSON_Delete(cjArray);
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


int	StreamResults()
{
	CHILD_STAT_t	*chld;
	int				count  = 0;

	for(chld = childStatFreeQ; chld; chld = chld->next)
	{
		fprintf(debugParentFP,"Streaming %s\n",chld->childLogFile);
		fflush(debugParentFP);
		count += StreamFileByLine(chld->childLogFile);
	}

	WriteResponse("%s","");
	return count;
}


SSL_SESSION *GetSessionCB(SSL *ssl,unsigned char *sessid,int len,int *copy)
{
	SSL_SESSION	*sess;
	
	if(!REUSE)
		return NULL;

	fprintf(debugChildFP,"GetSessionCB:\n");
	sess = ASHOKE_TOOL_find_session(sessid,curChildStat->sessFile);
	fprintf(debugChildFP,"GetSessionCB: sess %p\n",sess);
	return sess;
}


static int		ResponseProfileOne(SSL *s)
{
	char	buf[] = "I AM DONE\n";
	char	tbuf[1024];
	char	*ptr;
	int		ret,len;

	len = strlen(buf);
	sprintf(tbuf,"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: %d\r\n\r\n", len);
	len = strlen(tbuf);
	tbuf[len] = 0;
	strcat(tbuf,buf);

	len = strlen(tbuf);
	ptr = tbuf;
	while(len)
	{
		ret = SSL_write(s,ptr,len);
		if(ret <= 0)
			break;
		len -= ret;
		ptr += ret;
	}
	return 0;
}


static int		ResponseProfileTwo(SSL *ssl)
{
	unsigned short s;
	int		ret,fd,sz,len;
	FILE	*fp,*fo;
	char	*buf;
	int		tot = 0;
	struct	stat sb;
	int		recsize = RECORDSIZE;
	int		respsize = RESPSIZE;
	int		delay = DELAY;
	char	*dataP = data_16384;
	int		dataSize = 16384;

	char	tbuf[1024];
	sprintf(tbuf,"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: %d\r\n\r\n", respsize);

	len = strlen(tbuf);
	buf = tbuf;
	while(len)
	{
		if(recsize > len)
			recsize = len;

		ret = SSL_write(ssl,buf,recsize);
		if(ret <= 0)
			break;
		len -= ret;
		buf += ret;
	}


	recsize = RECORDSIZE;
	if(respsize < recsize)
		recsize = respsize;

	while(respsize)
	{
		int		ret, len;

		if(dataSize == 0)
		{
			dataP = data_16384;
			dataSize = 16384;
		}

		if(recsize > respsize)
			recsize = respsize;
		if(dataSize < recsize)
		{
			recsize = dataSize;
		}
		respsize -= recsize;

		len = recsize;
		while(len)
		{
			ret = SSL_write(ssl,dataP,len);
			if(ret <= 0)
				break;
			len -= ret;
			dataP += ret;
			dataSize -= ret;
		}

		if(len)
			break;
		Delay(delay);
	}
}



static int Delay(int i)
{
	FILE	*fp;
	char	c;

	fprintf(debugChildFP,"Delay(%d)\n",i);
	fflush(debugChildFP);

	while(i--)
	{
		fp = fopen("/mnt/ToolPkg/Server/delayfile.txt","r");
		setbuf(fp,NULL);
		while(!feof(fp))
		{
			fread(&c,1,1,fp);
		}
		fclose(fp);
	}
	return 0;
}
