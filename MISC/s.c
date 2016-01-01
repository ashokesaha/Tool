
#define	DOBUF(s)	switch(s->state) {\
						case SSL3_ST_CW_CERT_A:\
						case SSL3_ST_CW_CERT_B:\
						case SSL3_ST_CW_CERT_C:\
						case SSL3_ST_CW_CERT_D:\
							if(IS_BUF_CC(s)) return 0;break;\
							\
						case SSL3_ST_CW_KEY_EXCH_A:\
						case SSL3_ST_CW_KEY_EXCH_B:\
							if(IS_BUF_CKE(s)) return 0;break;\
							\
						case SSL3_ST_CW_CERT_VRFY_A:\
						case SSL3_ST_CW_CERT_VRFY_B:\
							if(IS_BUF_CCV(s)) return 0;break;\
					}\
