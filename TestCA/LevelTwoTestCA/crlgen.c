#include <stdio.h>
#include <errno.h>
#include <openssl/crypto.h>
#include <openssl/bio.h>
#include <openssl/stack.h>
#include <openssl/pem.h>

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
	unsigned long long		serial;
	int				endserial;
	int				inner,outer;
	unsigned long	seed;
	char			srl[8];
	int 			count;

	count = atoi(argv[1]);

	cacert 	= BIO_new(BIO_s_file());
	cakey 	= BIO_new(BIO_s_file());
	out 	= BIO_new(BIO_s_file());
	BIO_read_filename(cacert,CACERTNAME);
	BIO_read_filename(cakey,CAKEYNAME);
	BIO_write_filename(out,CRLOUT);


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

	seed = 0xA5A55A5A;
	srandom(seed);

	for(outer=0;outer<count;outer++)
	for(inner=0;inner<count;inner++)
	{
		serial = random();
		serial &= 0x7FFFFFFF;
		r = X509_REVOKED_new();
		X509_gmtime_adj(tmptm,-432000);
		X509_REVOKED_set_revocationDate(r,tmptm);

		ASN1_INTEGER_set(ai,(long)serial);
		X509_REVOKED_set_serialNumber(r,ai);
		X509_CRL_add0_revoked(crl,r);
		printf("serial %08x\n",serial);
	}

	serial = 0x0102030405;
	ASN1_INTEGER_set(ai,(long)serial);
	r = X509_REVOKED_new();
	X509_REVOKED_set_revocationDate(r,tmptm);
	X509_REVOKED_set_serialNumber(r,ai);
	X509_CRL_add0_revoked(crl,r);


	serial = 0x0102030405060708;
	ASN1_INTEGER_set(ai,serial);
	r = X509_REVOKED_new();
	X509_REVOKED_set_revocationDate(r,tmptm);
	X509_REVOKED_set_serialNumber(r,ai);
	X509_CRL_add0_revoked(crl,r);


	if (!X509_CRL_sign(crl,pkey,dgst))
	{
		printf("Failed to sign CRL\n");
		exit(1);
	}
	PEM_write_bio_X509_CRL(out,crl);
	ASN1_INTEGER_free(ai);
}
