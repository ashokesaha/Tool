#include <stdio.h>
#include <errno.h>
#include <openssl/crypto.h>
#include <openssl/bio.h>
#include <openssl/stack.h>
#include <openssl/pem.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>
#include <fcntl.h>


#define		CACERTNAME		"cacert.pem"
#define		CAKEYNAME		"cakey.pem"
#define		CRLDAYS			365
#define		CRLOUT			"crlfile"
#define		DIGEST			"MD5"

main(int argc,char **argv)
{
	BIO 			*cacert, *cakey, *out;
	EVP_PKEY		*pkey;
	X509			*x509;
	X509_REVOKED	*r;
	X509_CRL		*crl;
	ASN1_TIME		*tmptm;
	ASN1_INTEGER	*ai;
	const EVP_MD	*dgst;
	int				serial;
	int				endserial;
	int				inner,outer;
	unsigned long	seed;
	char			srl[8];
	int 			count;
	int				avgdepth;
	char			*crlname;
	char			filename[32];
	unsigned int	mask;
	int				fd;
	unsigned char   randData[8192];
	unsigned char 	*randDataPtr = randData;
	unsigned char 	*randDataEndPtr;
	BIGNUM			*bnSerial;

	count 		= atoi(argv[1]);
	avgdepth 	= atoi(argv[2]);
	crlname		= argv[3];

	cacert 	= BIO_new(BIO_s_file());
	cakey 	= BIO_new(BIO_s_file());
	out 	= BIO_new(BIO_s_file());

	//BIO_read_filename(cacert,CACERTNAME);
	//BIO_read_filename(cakey,CAKEYNAME);
	//BIO_write_filename(out,CRLOUT);

	sprintf(filename,"%s-cert.pem",crlname);
	BIO_read_filename(cacert,filename);
	sprintf(filename,"%s-key.pem",crlname);
	BIO_read_filename(cakey,filename);
	sprintf(filename,"%s-crl.pem",crlname);
	BIO_write_filename(out,filename);


	pkey = PEM_read_bio_PrivateKey(cakey,NULL,NULL,NULL);
	if(!pkey)
	{
		printf("cound not read cakey file \n");
		exit(1);
	}

	x509 = PEM_read_bio_X509(cacert,NULL,NULL,NULL);
	if(!x509)
	{
		printf("cound not read cacert file \n");
		exit(1);
	}

	crl = X509_CRL_new();
	
	tmptm = ASN1_TIME_new();
	X509_gmtime_adj(tmptm,0);
	X509_CRL_set_lastUpdate(crl,tmptm);	
	X509_gmtime_adj(tmptm,CRLDAYS*24*60*60);
	X509_CRL_set_nextUpdate(crl, tmptm);	

	X509_CRL_set_issuer_name(crl,X509_get_subject_name(x509));
	ai = ASN1_INTEGER_new();

	dgst = EVP_md5();
	if(!dgst)
	{
		printf("Could not find digest for %s\n",DIGEST);
		exit(1);
	}

#if 0
	seed = 0xA5A55A5A;
	srandom(seed);
	for(outer=0;outer<5;outer++)
	for(inner=0;inner<5;inner++)
	for(;serial<=endserial;serial++)
#endif

	fd = open("/dev/random",O_RDONLY);
	read(fd,randData,sizeof(randData));
	randDataPtr 	= randData;
	randDataEndPtr 	= randDataPtr + sizeof(randData);
	close(fd);

	//for(outer=0;outer<count;outer++)
	for(inner=0;inner<count;inner++)
	{
		if( (randDataEndPtr - randDataPtr) < avgdepth)
		{
			fd = open("/dev/random",O_RDONLY);
			read(fd,randData,8192);
			randDataPtr 	= randData;
			randDataEndPtr 	= randDataPtr + sizeof(randData);
			close(fd);
		}

		r = X509_REVOKED_new();
		X509_gmtime_adj(tmptm,-432000);
		X509_REVOKED_set_revocationDate(r,tmptm);

		//ASN1_INTEGER_set(ai,(long)serial);

		bnSerial = BN_bin2bn((const unsigned char *)randDataPtr,avgdepth,NULL);
		ai = BN_to_ASN1_INTEGER(bnSerial,NULL);
		randDataPtr += avgdepth;

		//ai = c2i_ASN1_UINTEGER(NULL,(const unsigned char **)(&randDataPtr),avgdepth);
		X509_REVOKED_set_serialNumber(r,ai);
		X509_CRL_add0_revoked(crl,r);

		//M_ASN1_INTEGER_free(ai);
		//printf("serial %08x\n",serial);
	}

	if (!X509_CRL_sign(crl,pkey,dgst))
	{
		printf("Failed to sign CRL\n");
		exit(1);
	}
	PEM_write_bio_X509_CRL(out,crl);
	ASN1_INTEGER_free(ai);
}
