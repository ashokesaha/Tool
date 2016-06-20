%{
#include <stdio.h>
#include <string.h>
#include "parser.h"

extern int yylex();
extern int yyparse();
extern FILE *yyin;
extern FILE *outfp;

extern	STMT_t			STMT;
extern	SET_ATTR_t		SetAttr;
extern  SSL_PARAMS_t	SSLParams;
extern	CTRIE_t			*ctrie_head;

extern	int 	rule_matched;
extern	int		PY;
extern	int		PL;
extern	int 	debugLine;
extern	int 	lineNo;
extern	int 	batchmode;
 
void yyerror(const char *str)
{
}
 
int yywrap()
{
	return 1;
}

main(int argc, char **argv)
{
	FILE *fp = fopen(argv[1],"r");
	//outfp = fopen(argv[2],"r");
	if(argv[2] && !strcmp(argv[2],"-b"))
		batchmode = 1;

	bzero(&SSLParams,sizeof(SSLParams));
	ctrie_head = (CTRIE_t *)Malloc(sizeof(CTRIE_t));
	ctrie_head->L = (LIST_t *)Malloc(sizeof(LIST_t));
	initList(ctrie_head->L,32);

	yyin = fp;
	do {
		yyparse();
	} while (!feof(yyin));

	//handleSSLParams(&SSLParams);
	PostParse();
	NameDynamicCipherGroup();
	nameProfile();
	PrintConfig();
} 

%}



%union {
	char *yy_data;	
	int	  yy_onoff;
	int	  yy_number;
}

%token  <yy_data>ADD SET BIND VSRVR SVC SVCGRP MODULE NAME WORD SSL SSLVERSION PSHENCTRG PSHENCTRGVAL
%token  <yy_data>CIPHERURL CLNTCERT DHFILE SSLPROF DTLSPROF SSLV2URL CMNNAME PUSHENCTRG
%token  <yy_data>CIPHERNAMETOK CIPHERTOK ECCCURVETOK PARAM_INSRTENCODING
%token  <yy_onoff>ONOFF CIPHERDRCT CLNTAUTH DH DHKEYEXPLIMIT ERSA NONFIPSCIPHER RDRCTPORTRW  YESNO
%token  <yy_onoff>SNDCN SESSREUSE SNI SSLRDRCT SSL2RDRCT SRVRAUTH PARAM_SNDCLOSENTFY
%token  <yy_onoff>SSL2 SSL3 TLS1 TLS11 TLS12 PARAM_DROPNOHOSTHDR PARAM_STRCTCACHK
%token  <yy_number>NUMBER CLRTXTPORT DHCOUNT ERSACOUNT SESSTIMEOUT SSLPARAM 
%token  <yy_number>PARAM_ENCRTRIGPKTCOUNT PARAM_PUSHTRIGTMOUT PARAM_PUSHFLG PARAM_QNTMSZ PARAM_TRGTMOUT SSLPARAM PARAM_CRLMEMSZ PARAM_OCSPCACHESZ 
%token  <yy_data>PARAM_DENYRENEG PARAM_UNDEFACTCTRL PARAM_UNDEFACTDATA VSRVRTOK  ORDTOK


%%
statements: statement          	{rule_matched=0; if(debugY())printf("Rule 1\n");}
	| statements statement   	{rule_matched=0; if(debugY())printf("Rule 2\n");}
	| error '\n'				{if(debugY())printf("Rule Error (%d)\n",lineNo);} 
	;



statement: confstmt WORDS '\n'	{if(debugY())printf("Rule 3\n");}
	| confstmt '\n' 			{if(debugY())printf("Rule 3.1\n");}
	;

confstmt:  
	ADD MODULE VSRVR NAME SSL
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.module,$2);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleAddVserver($2,$4,1);
		}
	| ADD SVC NAME NAME SSL
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$2);
			strcpy(STMT.name,$3);
			handleAddVserver($2,$3,0);
		}
	| ADD SVCGRP NAME SSL
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$2);
			handleAddVserver($2,$3,0);
		}
	| SET SSL VSRVR NAME SETSSLATTRIBS
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleSetVserver($4,&SetAttr,1);
		}
	| SET SSL SVC NAME SETSSLATTRIBS
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleSetVserver($4,&SetAttr,0);
		}
	| SET SSL SVCGRP NAME SETSSLATTRIBS
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleSetVserver($4,&SetAttr,0);
		}
	| SET SSL SSLPARAM SSLPARAMETERS
		{
			rule_matched = 1;
		}
	| BIND SSL VSRVR NAME CIPHERNAMETOK NAME
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleBindVserverCipher($4,$6,1);
		}
	| BIND SSL VSRVR NAME ECCCURVETOK NAME
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleBindVserverECCCurve($4,$6,1);
		}
	| BIND SSL SVC NAME CIPHERNAMETOK NAME
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleBindVserverCipher($4,$6,0);
		}
	| BIND SSL SVC NAME ECCCURVETOK NAME
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleBindVserverECCCurve($4,$6,0);
		}
	| BIND SSL SVCGRP NAME CIPHERNAMETOK NAME
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleBindVserverCipher($4,$6,0);
		}
	| BIND SSL SVCGRP NAME ECCCURVETOK NAME
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleBindVserverECCCurve($4,$6,0);
		}
	| ADD SSL CIPHERTOK NAME 
		{
			printf("Cipher Rule..\n");
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleAddCipherGroup($4);
		}
	| ADD SSL CIPHERTOK NAME NAME
		{
			printf("Cipher Rule 2..\n");
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleAddCipherGroupOld($4,$5);
		}
	| BIND SSL CIPHERTOK NAME CIPHERNAMETOK NAME
		{
			rule_matched = 1;
			bzero(&STMT,sizeof(STMT));
			strcpy(STMT.cmd,$1);
			strcpy(STMT.entity,$3);
			strcpy(STMT.name,$4);
			handleBindCipherGroup($4,$6);
		}
	| BIND SSL CIPHERTOK NAME VSRVRTOK ORDTOK NAME
		{

		}
	;


SETSSLATTRIBS: SETONESSLATTRIB
	| SETONESSLATTRIB SETSSLATTRIBS
	;


SETONESSLATTRIB : 
		  CIPHERDRCT	ONOFF   { if(debugY())printf("Rule: CIPHERDRCT ONOFF(%d)\n",yylval.yy_onoff); ATTRONOFF(cipherRedirect);}
		| CLNTAUTH		ONOFF   { if(debugY())printf("Rule: CLNTAUTH ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(clientAuth);}
		| DH			ONOFF   { if(debugY())printf("Rule: DH ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(dh);}
		| DHKEYEXPLIMIT	ONOFF   { if(debugY())printf("Rule: DHKEYEXPLIMIT ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(dhKeyExpSizeLimit);}
		| ERSA			ONOFF   { if(debugY())printf("Rule: ERSA ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(eRSA);}
		| NONFIPSCIPHER	ONOFF   { if(debugY())printf("Rule: NONFIPSCIPHER ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(nonFipsCiphers);}
		| RDRCTPORTRW	ONOFF   { if(debugY())printf("Rule: RDRCTPORTRW ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(redirectPortRewrite);}
		| SNDCN			YESNO   { if(debugY())printf("Rule: SNDCN ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(sendCloseNotify);}
		| SESSREUSE		ONOFF   { if(debugY())printf("Rule: SESSREUSE ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(sessReuse);}
		| SNI			ONOFF   { if(debugY())printf("Rule: SNI ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(SNIEnable);}
		| SSLRDRCT		ONOFF   { if(debugY())printf("Rule: SSLRDRCT ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(sslRedirect);}
		| SSL2RDRCT		ONOFF   { if(debugY())printf("Rule: SSL2RDRCT ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(sslv2Redirect);}
		| SRVRAUTH		ONOFF   { if(debugY())printf("Rule: SRVRAUTH ONOFF(%d)\n",yylval.yy_onoff);ATTRONOFF(serverAuth);}
		| SSLVERSION	ONOFF   { 
				if(debugY())printf("Rule: SSLVERSION ONOFF(%d)\n",yylval.yy_onoff); 
				if(strcmp($1,"-ssl2")==0)       {ATTRONOFF(ssl2);}
				else if(strcmp($1,"-ssl3")==0)  {ATTRONOFF(ssl3);}
				else if(strcmp($1,"-tls1")==0)  {ATTRONOFF(tls1);}
				else if(strcmp($1,"-tls11")==0) {ATTRONOFF(tls11);}
				else if(strcmp($1,"-tls12")==0) {ATTRONOFF(tls12);}
			}
		| CLRTXTPORT	NUMBER  { if(debugY())printf("Rule: CLRTXTPORT NUMBER(%d)\n",yylval.yy_onoff);SetAttr.core._clearTextPort = yylval.yy_onoff;SetAttr.U.bits._clearTextPort=1;}
		| DHCOUNT		NUMBER  { if(debugY())printf("Rule: DHCOUNT NUMBER(%d)\n",yylval.yy_onoff);SetAttr.core._dhCount = yylval.yy_onoff;SetAttr.U.bits._dhCount=1;}
		| ERSACOUNT		NUMBER  { if(debugY())printf("Rule: ERSACOUNT NUMBER(%d)\n",yylval.yy_onoff);SetAttr.core._eRSACount = yylval.yy_onoff;SetAttr.U.bits._eRSACount=1;}
		| SESSTIMEOUT	NUMBER  { if(debugY())printf("Rule: SESSTIMEOUT NUMBER(%d)\n",yylval.yy_onoff);SetAttr.core._sessTimeout = yylval.yy_onoff;SetAttr.U.bits._sessTimeout=1;}
		| CIPHERURL		NAME    { if(debugY())printf("Rule: CIPHERURL NAME(%s)\n",$2);strcpy(SetAttr.core._cipherURL, $2);SetAttr.U.bits._cipherURL=1;}
		| CLNTCERT		NAME    { if(debugY())printf("Rule: CLNTCERT NAME(%s)\n",$2);strcpy(SetAttr.core._clientCert,$2);SetAttr.U.bits._clientCert=1;}
		| DHFILE		NAME    { if(debugY())printf("Rule: DHFILE NAME(%s)\n",$2);strcpy(SetAttr.core._dhFile,$2);SetAttr.U.bits._dhFile=1;}
		| SSLPROF		NAME    { if(debugY())printf("Rule: SSLPROF NAME(%s)\n",$2);strcpy(SetAttr.core._sslProfile,$2);SetAttr.U.bits._sslProfile=1;}
		| DTLSPROF		NAME    { if(debugY())printf("Rule: DTLSPROF NAME(%s)\n",$2);strcpy(SetAttr.core._dtlsProfileName,$2);SetAttr.U.bits._dtlsProfileName=1;}
		| SSLV2URL		NAME    { if(debugY())printf("Rule: SSLV2URL NAME(%s)\n",$2);strcpy(SetAttr.core._sslv2URL,$2);SetAttr.U.bits._sslv2URL=1;}
		| CMNNAME		NAME    { if(debugY())printf("Rule: CMNNAME NAME(%s)\n",$2);strcpy(SetAttr.core._commonName,$2);SetAttr.U.bits._commonName=1;}
		| PSHENCTRG		PSHENCTRGVAL    { if(debugY())printf("Rule: PSHENCTRG PSHENCTRGVAL(%s)\n",$2);strcpy(SetAttr.core._pushEncTrigger,$2);SetAttr.U.bits._pushEncTrigger=1;}
		;




SSLPARAMETERS: SSLONEPARAM
	| SSLONEPARAM SSLPARAMETERS
	;

SSLONEPARAM : 
		  PARAM_DENYRENEG	NAME   { if(debugY())printf("Rule: PARAM_DENYRENEG WORD(%s)\n",$2); SSLParams.param_core.denySSLReneg = strdup($2);SSLParams.P.param_bits._denySSLReneg=1;}

		  | PARAM_DROPNOHOSTHDR	YESNO   { if(debugY())printf("Rule: PARAM_DROPNOHOSTHDR WORD(%d)\n",yylval.yy_onoff); SSLParams.param_core.dropReqWithNoHostHeader = yylval.yy_onoff;SSLParams.P.param_bits._dropReqWithNoHostHeader=1;}

		  | PARAM_ENCRTRIGPKTCOUNT	NUMBER   { if(debugY())printf("Rule: PARAM_ENCRTRIGPKTCOUNT NUMBER(%d)\n",yylval.yy_onoff); SSLParams.param_core.encryptTriggerPktCount = yylval.yy_onoff;SSLParams.P.param_bits._encryptTriggerPktCount=1;}

		  | PARAM_INSRTENCODING	NAME   { if(debugY())printf("Rule: PARAM_INSRTENCODING NAME(%s)\n",$2); SSLParams.param_core.insertionEncoding = strdup($2);SSLParams.P.param_bits._insertionEncoding=1;}

		  | PARAM_PUSHTRIGTMOUT	NUMBER   { if(debugY())printf("Rule: PARAM_PUSHTRIGTMOUT NUMBER(%d)\n",yylval.yy_number); SSLParams.param_core.pushEncTriggerTimeout = yylval.yy_number;SSLParams.P.param_bits._pushEncTriggerTimeout=1;}

		  | PARAM_PUSHFLG	NUMBER   { if(debugY())printf("Rule: PARAM_PUSHFLG NUMBER(%d)\n", yylval.yy_onoff); SSLParams.param_core.pushFlag = yylval.yy_onoff;SSLParams.P.param_bits._pushFlag=1;}

		  | PARAM_QNTMSZ	NUMBER   { if(debugY()) printf("Rule: PARAM_QNTMSZ NUMBER(%d)\n",yylval.yy_number); SSLParams.param_core.quantumSize = yylval.yy_number;SSLParams.P.param_bits._quantumSize=1;}

		  | PARAM_SNDCLOSENTFY	YESNO   { if(debugY())printf("Rule: PARAM_SNDCLOSENTFY YESNO(%d)\n",yylval.yy_onoff); SSLParams.param_core.sendCloseNotify = yylval.yy_onoff;SSLParams.P.param_bits._sendCloseNotify=1;}

		  | PARAM_TRGTMOUT	NUMBER   { if(debugY())printf("Rule: PARAM_TRGTMOUT NUMBER(%d)\n",yylval.yy_number); SSLParams.param_core.sslTriggerTimeout = yylval.yy_number;SSLParams.P.param_bits._sslTriggerTimeout=1;}

		  | PARAM_STRCTCACHK	YESNO   { if(debugY())printf("Rule: PARAM_STRCTCACHK YESNO(%d)\n",yylval.yy_onoff); SSLParams.param_core.strictCAChecks = yylval.yy_onoff;SSLParams.P.param_bits._strictCAChecks=1;}

		  | PARAM_CRLMEMSZ	NUMBER   { if(debugY())printf("Rule: PARAM_CRLMEMSZ NUMBER(%d)\n",yylval.yy_number);}

		  | PARAM_OCSPCACHESZ	NUMBER   { if(debugY())printf("Rule: PARAM_OCSPCACHESZ NUMBER(%d)\n",yylval.yy_number);}

		  | PARAM_UNDEFACTCTRL	NAME   { if(debugY())printf("Rule: PARAM_UNDEFACTCTRL NAME(%s)\n",$2);}

		  | PARAM_UNDEFACTDATA	NAME   { if(debugY())printf("Rule: PARAM_UNDEFACTDATA NAME($2)\n",$2);}
		;



WORDS:				{if(debugY())printf("WORDS []\n");} 
	   WORD			{if(debugY())printf("WORDS [WORD]\n");}
	|  WORDS WORD	{if(debugY())printf("WORDS [WORDS WORD]\n");}
	|  '\n'			{if(debugY())printf("WORDS [\\n]\n");}
	;

%%
