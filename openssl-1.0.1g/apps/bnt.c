#include "openssl/bn.h"


main()
{
	unsigned char D[] = {0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0a,0x0b};
	BIGNUM	*a,*b;
	unsigned char buf[256];
	int i,j,k,l;

	a = BN_bin2bn(D,sizeof(D),NULL);
	BN_add_word(a,0x100);
	l = BN_bn2bin(a,buf);
	for(i=0;i<l;i++)
		printf("%02x ",buf[i]);
	printf("\n\n");
}
