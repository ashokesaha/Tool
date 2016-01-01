#include "openssl/opensslconf.h"
#include "openssl/crypto.h"
#include "openssl/evp.h"
#include "openssl/err.h"
#include "string.h"
#include "assert.h"
#include "openssl/aes.h"
#include "crypto/evp/evp_locl.h"
#include "crypto/modes/modes_lcl.h"
#include "openssl/rand.h"

static const u8 K1[16]; 
static u8 *P1 = NULL; 
static u8 *A1 = NULL; 
static u8 IV1[12]; 
static u8 *C1 = NULL;

static const u8 T1[] = {
    0x58, 0xe2, 0xfc, 0xce, 0xfa, 0x7e, 0x30, 0x61,
    0x36, 0x7f, 0x1d, 0x57, 0xa4, 0xe7, 0x45, 0x5a
	};

int main()
{
    GCM128_CONTEXT ctx;
    AES_KEY key;
    int ret = 0;

    do 
	{ 

	u8 out[sizeof(P1)]; 
	AES_set_encrypt_key(K1,sizeof(K1)*8,&key); 
	CRYPTO_gcm128_init(&ctx,&key,(block128_f)AES_encrypt); 
	CRYPTO_gcm128_setiv(&ctx,IV1,sizeof(IV1)); 
	memset(out,0,sizeof(out)); 

	if (A1) 
		CRYPTO_gcm128_aad(&ctx,A1,sizeof(A1)); 

	if (P1) 
		CRYPTO_gcm128_encrypt(&ctx,P1,out,sizeof(out)); 

	if (CRYPTO_gcm128_finish(&ctx,T1,16) || (C1 && memcmp(out,C1,sizeof(out))))
	{
		ret++;
		printf ("encrypt test#%d failed.\n",1); 
	}

	CRYPTO_gcm128_setiv(&ctx,IV1,sizeof(IV1)); 
	memset(out,0,sizeof(out)); 
	if (A1) 
		CRYPTO_gcm128_aad(&ctx,A1,sizeof(A1)); 
	if (C1) 
		CRYPTO_gcm128_decrypt(&ctx,C1,out,sizeof(out)); 

	if (CRYPTO_gcm128_finish(&ctx,T1,16) || (P1 && memcmp(out,P1,sizeof(out))))
	{
		ret++;
		printf ("decrypt test#%d failed.\n",1);
	}

	} while(0);

	return 0;
}
