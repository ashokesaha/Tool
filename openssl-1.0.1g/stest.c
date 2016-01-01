#include <stdio.h>
#include <strings.h>
#include <string.h>
#include "openssl/pem.h"
#include "openssl/rsa.h"

#define	INPUT	"iamashoke"


main(int argc, char **argv)
{
	char	*cfile = argv[1];
	char	tbuf[64];
	char	*kfile = argv[2];
	FILE	*fp,*kfp;
	unsigned char	*out;
	int		i,count = atoi(argv[3]);

	X509		*x;
	RSA			*r;
	EVP_PKEY	*e;

	BN_CTX		*ctx = BN_CTX_new();

	BN_CTX_init(ctx);
	BIGNUM	*mr,*ma,*mb,*dv,*rm,*mm;

	//printf("char %d\n",sizeof(char));
	//printf("short %d\n",sizeof(short));
	//printf("int %d\n",sizeof(int));
	//printf("long %d\n",sizeof(long));

	fp  = fopen(cfile,"r");
	kfp = fopen(kfile,"r");
	if(!fp || !kfp)
	{
		printf("Failed to open files\n");
		exit(0);
	}

	x = PEM_read_X509(fp,NULL,NULL,NULL);
	if(!x)
	{
		printf("Failed to parse cert\n");
		exit(0);
	}

	r = PEM_read_RSAPrivateKey(kfp,NULL,NULL,NULL);
	if(!r)
	{
		printf("Failed to parse key\n");
		exit(0);
	}

	out = malloc(RSA_size(r));
	if(!out)
	{
		printf("Failed to alloc memory\n");
		exit(0);
	}

	e = X509_PUBKEY_get(x->cert_info->key);

	mr = BN_new();
	ma = BN_new();
	mb = BN_new();
	mm = BN_new();
	dv = BN_new();
	rm = BN_new();

	BN_rand(ma,2048,0,1);
	BN_rand(mb,2048,0,1);
	BN_rand(mm,2040,0,1);

	/****************************************************
	RSA_public_encrypt(strlen(INPUT),INPUT,out,e->pkey.rsa,RSA_PKCS1_PADDING);
	for(i=0;i<count;i++)
	{
		bzero(tbuf,sizeof(tbuf));
		RSA_public_encrypt(strlen(INPUT),INPUT,out,e->pkey.rsa,RSA_PKCS1_PADDING);
		RSA_private_decrypt(RSA_size(r),out,tbuf,r,RSA_PKCS1_PADDING);
		printf("tbuf: %s\n",tbuf);
	}
	****************************************************/


	/***********************
	for(i=0;i<count;i++)
	{
		BN_CTX_init(ctx);
		if(!BN_mul(mr,ma,mb,ctx))
		{
			printf("BN_mul error :\n");
			exit(0);
		}
		BN_CTX_init(ctx);
		if(!BN_div(dv,rm,mr,mm,ctx))
		{
			printf("BN_mul error :\n");
			exit(0);
		}
		BN_copy(mb,dv);
		BN_add(ma,ma,rm);
	}
	***********************/

	for(i=0;i<count;i++)
	{
		BN_CTX_init(ctx);
		if(!BN_mod_exp(mr,ma,mb,mm,ctx))
		{
			printf("BN_mul error :\n");
			exit(0);
		}
		BN_copy(ma,mr);
	}

}
