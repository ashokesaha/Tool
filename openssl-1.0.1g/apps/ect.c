#include "openssl/bn.h"
#include "openssl/ec.h"
#include "../crypto/ec/ec_lcl.h" 
#include "openssl/ecdh.h"
#include "openssl/obj_mac.h"

main()
{
	unsigned char buf[1024];
	int	i,l;

	BN_CTX	*bn_ctx = BN_CTX_new();
	EC_GROUP *grp = EC_GROUP_new_by_curve_name(NID_X9_62_prime256v1);
	EC_POINT	*r,*g;

	BIGNUM	*scalar = BN_new();
	BN_zero(scalar);
	BN_add_word(scalar,2);

	BN_CTX_init(bn_ctx);
	r = EC_POINT_new(grp);
	g = EC_POINT_new(grp);

	EC_POINT_mul(grp,r,NULL,grp->generator,scalar,bn_ctx);
	//EC_POINT_mul(grp,r,scalar,NULL,NULL,bn_ctx);
	//EC_POINT_dbl(grp,r,grp->generator,bn_ctx);

	/*********************************
	l = BN_bn2bin(&grp->generator->X,buf);
	printf("generator X:\n");
	for(i=0;i<l;i++)
		printf("%02x ",buf[i]);
	printf("\n");

	l = BN_bn2bin(&grp->generator->Y,buf);
	printf("generator X:\n");
	for(i=0;i<l;i++)
		printf("%02x ",buf[i]);
	printf("\n");
	*********************************/

	printf("\n\n");	

	l = BN_bn2bin(&r->X,buf);
	printf("result X:\n");
	for(i=0;i<l;i++)
		printf("%02x ",buf[i]);
	printf("\n");

	l = BN_bn2bin(&r->Y,buf);
	printf("result Y:\n");
	for(i=0;i<l;i++)
		printf("%02x ",buf[i]);
	printf("\n\n");
}
