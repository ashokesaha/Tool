#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include <sys/wait.h>
#include <sys/time.h>
#include <openssl/ossl_typ.h>
#include <openssl/bio.h>
#include <openssl/ssl.h>
#include <openssl/dh.h>



typedef struct _cert_list_ {
	X509		*s_cert;
	EVP_PKEY	*s_key;
} CERT_LIST_t;

CERT_LIST_t	gCertList[1024];
int			gNumCertKey = 0;


SSL_CTX *newCTX();
int		loadCerts();
int 	initSocket(char *ip, int port);


#define		MAXCHILD	4

int main(int argc, char **argv)
{
	char	*IP = argv[1];
	int		PORT = atoi(argv[2]);
	int		asd, sd;
	int		len, childCount;
	int		pid = -1;
	int		status = 0, ret;

	struct	sockaddr_in	from;

	if(loadCerts() <= 0)
	{
		printf("Failed to load even a single cert..\n");
		exit(0);
	}
	printf("Loaded %d cert/key\n", gNumCertKey);

	asd = initSocket(IP,PORT);
	listen(asd,5);
	len = sizeof(from);

	childCount = 0;
	while(1)
	{
		sd = accept(asd,(struct sockaddr *)&from,(void *)&len);
		if(sd <= 0)
		{
			perror("accept::");
			exit(0);
		}

		pid = fork();
		if(pid > 0)
		{
			childCount++;
			while( (wait4(-1,&status,WNOHANG,NULL) > 0) )
				childCount--;

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
			ret = doChild(sd);
			exit(ret);
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

	ret = SSL_accept(con);
	if(ret <= 0)
		return -5;

	ret = SSL_read(con,buf,sizeof(buf)-1);
	if(ret <= 0)
		return -6;

	strcpy(obuf,"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 10\r\n\r\n1234567890");
	SSL_write(con,obuf,strlen(obuf));

	ssl3_send_alert(con,SSL3_AL_WARNING,SSL_AD_CLOSE_NOTIFY);

	ret = SSL_read(con,buf,sizeof(buf)-1);
	printf("second read : ret %d\n", ret);
	if(ret > 0)
	{
		printf("second read: [%s]\n", buf);
	}



	SSL_shutdown(con);
	return 0;
}





SSL_CTX *newCTX()
{
	SSL_CTX		*ctx;
	DH			*dh;
	const SSL_METHOD *meth=NULL;
	int		certId;
	struct timeval tv;

	SSL_load_error_strings();
	SSL_library_init();
	meth = TLSv1_server_method();

	ctx = SSL_CTX_new(meth);

	SSL_CTX_set_options(ctx,SSL_OP_ALL);

	SSL_CTX_sess_set_cache_size(ctx,128);

	//SSL_CTX_load_verify_locations(ctx,"RootServer2048CACert.pem","./");
	//dh = load_dh_param("dh_2048");
	//SSL_CTX_set_tmp_dh(ctx,dh);


	gettimeofday(&tv,NULL);
	srandom(tv.tv_usec);
	certId = random() % gNumCertKey;
	
	SSL_CTX_use_certificate(ctx,gCertList[certId].s_cert);
	SSL_CTX_use_PrivateKey(ctx,gCertList[certId].s_key);

	return ctx;
}



int	loadCerts()
{
	char	certName[64];
	char	keyName[64];
	int		i = 1, x;

	struct	stat sb;
	BIO		*cert;
	BIO		*key;

	for(x = 0; x < sizeof(gCertList)/sizeof(gCertList[0]); x++)
	{
		gCertList[x].s_cert = NULL;
		gCertList[x].s_key  = NULL;
	}

	while(i)
	{
		sprintf(certName,"intercept_%d_cert.pem",i);
		sprintf(keyName,"intercept_%d_key.pem",i);

		if((stat(certName,&sb)==-1) || (stat(keyName,&sb)==-1))
			break;
		i++;

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

		BIO_free(cert);
		BIO_free(key);

		gNumCertKey++;
	}
	return gNumCertKey;
}




int 	initSocket(char *ip, int port)
{
	int	s = -1;
	struct sockaddr_in server;

	s = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
	memset((char *)&server,0,sizeof(server));
	server.sin_family=AF_INET;
	server.sin_port=htons((unsigned short)port);
	server.sin_addr.s_addr = inet_addr(ip);	

	if (bind(s,(struct sockaddr *)&server,sizeof(server)) == -1)
	{
		perror("bind::");
		s = -1;
	}

	return s;
}
