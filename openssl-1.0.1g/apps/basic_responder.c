#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <signal.h>
#include <errno.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <openssl/ossl_typ.h>
#include <openssl/bio.h>
#include <openssl/ssl.h>
#include <openssl/dh.h>
#include <openssl/ec.h>
#include <openssl/bio.h>
#include <sys/select.h>
#include "cJSON.h"
#include "apps.h"


static int	HandleArgs(char * buf);
static int	DoResponder();
static int	send_ocsp_response(int ,OCSP_RESPONSE *);
static char **lookup_serial(CA_DB *,ASN1_INTEGER *);
static int	make_ocsp_response(OCSP_RESPONSE **,OCSP_REQUEST *,CA_DB *,
			X509 *,X509 *,EVP_PKEY *, STACK_OF(X509) *,unsigned long ,
			int,int);
static int unpack_revinfo_pvt(ASN1_TIME **prevtm, int *preason, ASN1_OBJECT **phold, ASN1_GENERALIZEDTIME **pinvtm, const char *str);


int			PORT = 0;
int			DELAY = 0;
char		*RSIGNERFILE = NULL;
char		*RKEYFILE = NULL;
char		*INDEXFILE = NULL;
char		*OCSPCADIR = NULL;
X509		*RSIGNER;
EVP_PKEY	*RKEY;
CA_DB		*RDB = NULL;
BIO			*BIO_ERR = NULL;

extern FILE *childLogFP;

static const char *crl_reasons[] = {
	/* CRL reason strings */
	"unspecified",
	"keyCompromise",
	"CACompromise",
	"affiliationChanged",
	"superseded", 
	"cessationOfOperation",
	"certificateHold",
	"removeFromCRL",
	/* Additional pseudo reasons */
	"holdInstruction",
	"keyTime",
	"CAkeyTime"
};
#define NUM_REASONS (sizeof(crl_reasons) / sizeof(char *))

extern FILE *parentLogFP;
int main(int argc, char **argv)
{
	SSL_load_error_strings();
	OpenSSL_add_ssl_algorithms();

	SetLogFile("ocsp.parent");
	INDEXFILE = "index.txt";
	SetCHDIR("/mnt/ToolPkg/OCSP");
	SetFirstResp("ocspresponder");
	SetArgHandler(HandleArgs);
	SetTestHandler(DoResponder);
	SetChildCount(1);

	ServerRun();
}


#if 0
int main()
{
	PORT = 5558;
	INDEXFILE = "index.txt";
	RSIGNERFILE = "BANGALORECA_cacert.pem";
	RKEYFILE = "BANGALORECA_cakey.pem";
	chdir("/mnt/ToolPkg/OCSP/BANGALORECA");

	childLogFP = fopen("/tmp/ocsp.log","w");
	setbuf(childLogFP,NULL);

	SSL_load_error_strings();
	OpenSSL_add_ssl_algorithms();

	RDB = load_index(INDEXFILE, NULL);
	if(!RDB)
		return -1;
	if (!index_index(RDB)) return -1;

	RSIGNER = load_cert(BIO_ERR,RSIGNERFILE,FORMAT_PEM,NULL,NULL,"resp cert");
	if(!RSIGNER)
		return -1;

	RKEY = load_key(BIO_ERR,RKEYFILE,FORMAT_PEM,0,NULL,NULL,"resp key");
	if(!RKEY)
		return -1;

	DoResponder();
}
#endif


int	DoResponder()
{
	int				x,ret=0,sd,asd=-1,len;
	unsigned char 	buf[8 * 1024];
	unsigned char	headerend[] = "\r\n\r\n";
	unsigned char	*ptr;
	fd_set			readfds;
	OCSP_REQUEST	*req = NULL;
	OCSP_RESPONSE	*resp = NULL;
	BIO				*biom = NULL;
	struct timeval	tv;

	tv.tv_sec = 0;
	tv.tv_usec = 500 * 1024;

	sd  = ServerSocket(NULL,PORT);
	listen(sd,5);

	while(1)
	{
		FD_ZERO(&readfds);
		FD_SET(sd,&readfds);	

fprintf(childLogFP,"DoResponder: going to select..\n");
		select(sd+1,&readfds,NULL,NULL,NULL);
fprintf(childLogFP,"DoResponder: out of select..\n");

		len = 0;
		if(FD_ISSET(sd,&readfds))
		{
			asd = accept(sd,NULL,&len);
		}

fprintf(childLogFP,"DoResponder: asd %d ..\n",asd);
		if(asd <= 0)
		{
			goto cleanall;
		}

		setsockopt(asd,SOL_SOCKET,SO_RCVTIMEO,&tv,sizeof(tv));
		len = recv(asd,buf,sizeof(buf),0);
fprintf(childLogFP,"OCSP Req len %d\n",len);
		if(len <= 0)
		{
			fprintf(childLogFP,"OCSP Req mesg read failure\n");
			goto cleanall;
		}

		ptr = buf;
		for(; len > 0; len--,ptr++)
		{
			if((*ptr == '\r') && !bcmp(ptr,headerend,strlen(headerend)))
			{
				len -= 4;
				ptr += 4;
				break;
			}
		}
		if(len <= 0)
		{
			fprintf(childLogFP,"Malformed HTTP OCSP Req \n");
			goto cleanall;
		}
		
		for(x=0; x<len; x++)
		{
			if(x%16 == 0) fprintf(childLogFP, "\n");
			fprintf(childLogFP, "%02x ",ptr[x]);
		}
		fprintf(childLogFP,"\n");

		biom = BIO_new_mem_buf(ptr,len);
		req = d2i_OCSP_REQUEST_bio(biom, NULL);
		if(!req)
		{
			fprintf(childLogFP,"Malformed OCSP Req \n");
			resp = OCSP_response_create(OCSP_RESPONSE_STATUS_MALFORMEDREQUEST, NULL);
			send_ocsp_response(asd, resp);
			goto cleanall;
		}
		fprintf(childLogFP,"Received OCSP Req \n");

		make_ocsp_response(&resp,req,RDB,RSIGNER,RSIGNER,RKEY,NULL,0,10,1);

		if(DELAY)
			usleep(DELAY * 1024);
		send_ocsp_response(asd, resp);


cleanall :
		if(asd > 0)
		{
			close(asd);
			asd = -1;
		}
		if(resp)
		{
			OCSP_RESPONSE_free(resp);
			resp = NULL;
		}
		if(req)
		{
			OCSP_REQUEST_free(req);
			req = NULL;
		}
		if(biom)
		{
			BIO_free_all(biom);
			biom = NULL;
		}
	}
fprintf(childLogFP,"DoResponder: exiting while..\n");

	return ret;
}





static int	HandleArgs(char * buf)
{
	int		i,ret;
	cJSON	*cJ, *cJc;

	if(!BIO_ERR)
	{
		BIO_ERR = BIO_new(BIO_s_file());
		BIO_set_fp(BIO_ERR,childLogFP,BIO_NOCLOSE);
	}

	if(buf[0] == '[')
		bcopy(buf+1,buf,strlen(buf)-1);

	cJ  = cJSON_Parse(buf);
	if(!cJ)
	{
		WriteResponse("cJSON_Parse failed\n");
		fflush(stderr);
		fprintf(parentLogFP,"HandleArgs: cJSON_Parse failed\n");
		fclose(parentLogFP);
		exit(0);
	}

	cJc = cJ->child;
	while(cJc)
	{
		if(strcmp(cJc->string,"port") == 0)
		{
			PORT = atoi(cJc->valuestring);
		}
	 	else if(strcmp(cJc->string,"delay") == 0)
		{
			DELAY = atoi(cJc->valuestring);
		}
	 	else if(strcmp(cJc->string,"rsigner") == 0)
		{
			RSIGNERFILE = strdup(cJc->valuestring);
		}
	 	else if(strcmp(cJc->string,"rkey") == 0)
		{
			RKEYFILE = strdup(cJc->valuestring);
		}
	 	else if(strcmp(cJc->string,"indexfile") == 0)
		{
			INDEXFILE = strdup(cJc->valuestring);
		}
	 	else if(strcmp(cJc->string,"cbName") == 0)
		{
			char	newdir[128];
			OCSPCADIR = strdup(cJc->valuestring);
			sprintf(newdir,"/mnt/ToolPkg/OCSP/%s",OCSPCADIR);
			SetCHDIR(newdir);
			fprintf(parentLogFP,"changed dir to %s\n",newdir);

			sprintf(newdir,"%s_cacert.pem",OCSPCADIR);
			RSIGNERFILE = strdup(newdir);
			sprintf(newdir,"%s_cakey.pem",OCSPCADIR);
			RKEYFILE = strdup(newdir);
			fprintf(parentLogFP,"RSIGNERFILE %s RKEYFILE %s\n",RSIGNERFILE,RKEYFILE);
		}
		cJc = cJc->next;
	}

	RDB = load_index(INDEXFILE, NULL);
	if(!RDB)
	{
		fprintf(parentLogFP,"load_index failed..\n");
		return -1;
	}
	if (!index_index(RDB)) 
		return -1;

	RSIGNER = load_cert(BIO_ERR,RSIGNERFILE,FORMAT_PEM,NULL,NULL,"resp cert");
	if(!RSIGNER)
	{
		fprintf(parentLogFP,"load RSIGNER failed..\n");
		return -1;
	}

	RKEY = load_key(BIO_ERR,RKEYFILE,FORMAT_PEM,0,NULL,NULL,"resp key");
	if(!RKEY)
	{
		fprintf(parentLogFP,"load RSIGNER failed..\n");
		return -1;
	}
	return 0;
}



static int send_ocsp_response(int asd, OCSP_RESPONSE *resp)
{
	int				ret,l1,l2,len;
	unsigned char 	buf[8192];
	char 			http_resp[256];
	unsigned char 	*ptr;

	ptr = buf;
	len = i2d_OCSP_RESPONSE(resp,&ptr);
	sprintf(http_resp,
		"HTTP/1.0 200 OK\r\nContent-type: application/ocsp-response\r\n"
		"Content-Length: %d\r\n\r\n",len);

	l2 = strlen(http_resp);
	l1 = 0;
	while(l1 < l2)
	{
		ret = send(asd,&http_resp[l1],l2-l1,0);
		if(ret < 0)
			return ret;
		l1 += ret;	
	}

	l1 = 0;
	while(l1 < len)
	{
		ret = send(asd,&buf[l1],len-l1,0);
		if(ret < 0)
			return ret;
		l1 += ret;	
	}

	return len;
}




static int make_ocsp_response(OCSP_RESPONSE **resp, OCSP_REQUEST *req, CA_DB *db,
			X509 *ca, X509 *rcert, EVP_PKEY *rkey,
			STACK_OF(X509) *rother, unsigned long flags,
			int nmin, int ndays)
{
	ASN1_TIME *thisupd = NULL, *nextupd = NULL;
	OCSP_CERTID *cid, *ca_id = NULL;
	OCSP_BASICRESP *bs = NULL;
	int i, id_count, ret = 1;

	id_count = OCSP_request_onereq_count(req);

	if (id_count <= 0)
	{
		*resp = OCSP_response_create(OCSP_RESPONSE_STATUS_MALFORMEDREQUEST, NULL);
		goto end;
	}


	bs = OCSP_BASICRESP_new();
	thisupd = X509_gmtime_adj(NULL, 0);
	if (ndays != -1)
		nextupd = X509_gmtime_adj(NULL, nmin * 60 + ndays * 3600 * 24 );

	/* Examine each certificate id in the request */
	for (i = 0; i < id_count; i++)
	{
		OCSP_ONEREQ *one;
		ASN1_INTEGER *serial;
		char **inf;
		ASN1_OBJECT *cert_id_md_oid;
		const EVP_MD *cert_id_md;
		one = OCSP_request_onereq_get0(req, i);
		cid = OCSP_onereq_get0_id(one);

		OCSP_id_get0_info(NULL,&cert_id_md_oid, NULL,NULL, cid);

		cert_id_md = EVP_get_digestbyobj(cert_id_md_oid);	
		if (! cert_id_md) 
		{
			*resp = OCSP_response_create(OCSP_RESPONSE_STATUS_INTERNALERROR,NULL);
			goto end;
		}	

		if (ca_id) OCSP_CERTID_free(ca_id);
		ca_id = OCSP_cert_to_id(cert_id_md, NULL, ca);

		/* Is this request about our CA? */
		if (OCSP_id_issuer_cmp(ca_id, cid))
		{
			OCSP_basic_add1_status(bs, cid,
						V_OCSP_CERTSTATUS_UNKNOWN,
						0, NULL,
						thisupd, nextupd);
			continue;
		}

		OCSP_id_get0_info(NULL, NULL, NULL, &serial, cid);
		inf = lookup_serial(db, serial);
		if (!inf)
			OCSP_basic_add1_status(bs, cid,
						V_OCSP_CERTSTATUS_UNKNOWN,
						0, NULL,
						thisupd, nextupd);
		else if (inf[DB_type][0] == DB_TYPE_VAL)
			OCSP_basic_add1_status(bs, cid,
						V_OCSP_CERTSTATUS_GOOD,
						0, NULL,
						thisupd, nextupd);
		else if (inf[DB_type][0] == DB_TYPE_REV)
		{
			ASN1_OBJECT *inst = NULL;
			ASN1_TIME *revtm = NULL;
			ASN1_GENERALIZEDTIME *invtm = NULL;
			OCSP_SINGLERESP *single;
			int reason = -1;
			unpack_revinfo_pvt(&revtm, &reason, &inst, &invtm, inf[DB_rev_date]);
			single = OCSP_basic_add1_status(bs, cid,
						V_OCSP_CERTSTATUS_REVOKED,
						reason, revtm,
						thisupd, nextupd);
			if (invtm)
				OCSP_SINGLERESP_add1_ext_i2d(single, NID_invalidity_date, invtm, 0, 0);
			else if (inst)
				OCSP_SINGLERESP_add1_ext_i2d(single, NID_hold_instruction_code, inst, 0, 0);
			ASN1_OBJECT_free(inst);
			ASN1_TIME_free(revtm);
			ASN1_GENERALIZEDTIME_free(invtm);
		}
	}

	OCSP_copy_nonce(bs, req);
	
	OCSP_basic_sign(bs, rcert, rkey, NULL, rother, flags);

	*resp = OCSP_response_create(OCSP_RESPONSE_STATUS_SUCCESSFUL, bs);

	end:
	ASN1_TIME_free(thisupd);
	ASN1_TIME_free(nextupd);
	OCSP_CERTID_free(ca_id);
	OCSP_BASICRESP_free(bs);
	return ret;
}



static char **lookup_serial(CA_DB *db, ASN1_INTEGER *ser)
{
	int i;
	BIGNUM *bn = NULL;
	char *itmp, *row[DB_NUMBER],**rrow;
	for (i = 0; i < DB_NUMBER; i++) row[i] = NULL;
	bn = ASN1_INTEGER_to_BN(ser,NULL);
	OPENSSL_assert(bn); /* FIXME: should report an error at this point and abort */
	if (BN_is_zero(bn))
		itmp = BUF_strdup("00");
	else
		itmp = BN_bn2hex(bn);
	row[DB_serial] = itmp;
	BN_free(bn);
	rrow=TXT_DB_get_by_index(db->db,DB_serial,row);
	OPENSSL_free(itmp);
	return rrow;
}



static int unpack_revinfo_pvt(ASN1_TIME **prevtm, int *preason, ASN1_OBJECT **phold, ASN1_GENERALIZEDTIME **pinvtm, const char *str)
{
	char *tmp = NULL;
	char *rtime_str, *reason_str = NULL, *arg_str = NULL, *p;
	int reason_code = -1;
	int ret = 0;
	unsigned int i;
	ASN1_OBJECT *hold = NULL;
	ASN1_GENERALIZEDTIME *comp_time = NULL;
	tmp = BUF_strdup(str);

	p = strchr(tmp, ',');

	rtime_str = tmp;

	if (p)
	{
		*p = '\0';
		p++;
		reason_str = p;
		p = strchr(p, ',');
		if (p)
		{
			*p = '\0';
			arg_str = p + 1;
		}
	}

	if (prevtm)
	{
		*prevtm = ASN1_UTCTIME_new();
		if (!ASN1_UTCTIME_set_string(*prevtm, rtime_str))
		{
			BIO_printf(bio_err, "invalid revocation date %s\n", rtime_str);
			goto err;
		}
	}

	if (reason_str)
	{
		for (i = 0; i < NUM_REASONS; i++)
		{
			if(!strcasecmp(reason_str, crl_reasons[i]))
			{
				reason_code = i;
				break;
			}
		}

		if (reason_code == OCSP_REVOKED_STATUS_NOSTATUS)
		{
			BIO_printf(bio_err, "invalid reason code %s\n", reason_str);
			goto err;
		}

		if (reason_code == 7)
			reason_code = OCSP_REVOKED_STATUS_REMOVEFROMCRL;
		else if (reason_code == 8)		/* Hold instruction */
		{
			if (!arg_str)
			{	
				BIO_printf(bio_err, "missing hold instruction\n");
				goto err;
			}
			reason_code = OCSP_REVOKED_STATUS_CERTIFICATEHOLD;
			hold = OBJ_txt2obj(arg_str, 0);

			if (!hold)
			{
				BIO_printf(bio_err, "invalid object identifier %s\n", arg_str);
				goto err;
			}
			if (phold) *phold = hold;
		}
		else if ((reason_code == 9) || (reason_code == 10))
		{
			if (!arg_str)
			{	
				BIO_printf(bio_err, "missing compromised time\n");
				goto err;
			}
			comp_time = ASN1_GENERALIZEDTIME_new();
			if (!ASN1_GENERALIZEDTIME_set_string(comp_time, arg_str))
			{	
				BIO_printf(bio_err, "invalid compromised time %s\n", arg_str);
				goto err;
			}
			if (reason_code == 9)
				reason_code = OCSP_REVOKED_STATUS_KEYCOMPROMISE;
			else
				reason_code = OCSP_REVOKED_STATUS_CACOMPROMISE;
		}
	}

	if (preason) *preason = reason_code;
	if (pinvtm) *pinvtm = comp_time;
	else ASN1_GENERALIZEDTIME_free(comp_time);

	ret = 1;

	err:

	if (tmp) OPENSSL_free(tmp);
	if (!phold) ASN1_OBJECT_free(hold);
	if (!pinvtm) ASN1_GENERALIZEDTIME_free(comp_time);

	return ret;
}

