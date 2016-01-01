#include <stdio.h>
#include <strings.h>
#include <string.h>
#include "openssl/pem.h"
#include "openssl/bn.h"
#include "openssl/rsa.h"


main(int argc, char **argv)
{
	int	i,count = atoi(argv[1]);
	BIGNUM	*r,*a,*b;
	
	r = BN_new();
	a = BN_new();
	b = BN_new();

	BN_zero(r);
	BN_rand(a,4096,1,1);
	BN_rand(b,4096,1,1);

	for(i=0;i<count;i++)
	{
		BN_add(r,a,b);
		BN_add(a,r,b);
		BN_add(b,r,a);
	}
}
