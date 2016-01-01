#include <stdio.h>
#include <openssl/x509.h>
#include <openssl/pem.h>

main()
{
	FILE *fp;
	X509	*X;

	fp = fopen("cacert.der","r");
	X = d2i_X509_fp(fp,NULL);
	PEM_write_X509(stdout,X);
}
