%{
#include <string.h>
#include "y.tab.h"
#include "parser.h"

extern	SET_ATTR_t	SetAttr;
extern int rule_matched;
extern int lineNo;
extern int debugL();
extern STMT_t STMT;
extern int curstate;
%}


%s ADDSTATE SETSTATE SETSSLPARAM SETSSLPARAMDENYRENEG PSHENCTRGSTATE BINDSTATE ADDSSLSTATE 

%%
^add |
^ADD	{ yylval.yy_data = strdup(yytext); BEGIN ADDSTATE; curstate=ADDSTATE;return ADD;}

^set |
^SET	{ BEGIN SETSTATE; curstate=SETSTATE;yylval.yy_data = strdup(yytext); bzero(&SetAttr,sizeof(SetAttr));return SET;}

^bind |
^BIND	{ yylval.yy_data = strdup(yytext); BEGIN BINDSTATE; return BIND;}


lb  |
cs  |
cr  |
vpn |
LB  |
CS  |
CR  |
VPN	{
		int	mod = rule_matched ? WORD : MODULE;
		yylval.yy_data = strdup(yytext);
		if(debugL())
			printf("lex:%s(%s)\n",(mod==WORD)?"WORD":"MODULE",yytext);
		return mod;
	}


service  |
SERVICE  {
		int	mod = rule_matched ? WORD : SVC;
		yylval.yy_data = strdup(yytext);
		if(debugL())
			printf("lex:%s(%s)\n",(mod==WORD)?"WORD":"SVC",yytext);
		return mod;
		}

serviceGroup {
		int	mod = rule_matched ? WORD : SVCGRP;
		yylval.yy_data = strdup(yytext);
		if(debugL())
			printf("lex:%s(%s)\n",(mod==WORD)?"WORD":"SVCGRP",yytext);
		return mod;
		}


vserver  |
VSERVER {
		int	mod = rule_matched ? WORD : VSRVR;
		yylval.yy_data = strdup(yytext);
		if(debugL())
			printf("lex:%s(%s)\n",(mod==WORD)?"WORD":"VSRVR",yytext);
		return mod;
		}


-vServer {
		int	mod =  VSRVRTOK;
		yylval.yy_data = strdup(yytext);
		if(debugL())
			printf("lex:%s(%s)\n","VSRVRTOK",yytext);
		return mod;
		}


ORD {
		int	mod =  ORDTOK;
		yylval.yy_data = strdup(yytext);
		if(debugL())
			printf("lex:%s(%s)\n","ORDTOK",yytext);
		return mod;
		}


ssl  |
SSL  {
	int	mod = rule_matched ? WORD : SSL;
	yylval.yy_data = strdup(yytext);
	if(curstate == ADDSTATE) {BEGIN ADDSSLSTATE;curstate=0;};
	if(curstate == SETSTATE) {if(debugL()) printf("entered set ssl %d\n",lineNo);curstate=0;};
	if(debugL())
		printf("lex:%s(%s)\n",(mod==WORD)?"WORD":"SSL",yytext);
	return mod;
	}


<SETSSLPARAM>[0-9]+ | 
<SETSTATE>[0-9]+ {
	int	mod = NUMBER;
	yylval.yy_number = atoi(yytext);
	if(debugL())
		printf("lex:NUMBER(%d)\n",yylval.yy_number);
	return mod;
	}


<SETSSLPARAM>yes |
<SETSSLPARAM>YES |
<SETSTATE>yes |
<SETSTATE>YES {
	yylval.yy_onoff = 1;
	if(debugL())
		printf("lex:YESNO(%d)\n",yylval.yy_onoff);
	return YESNO;
	}


<SETSSLPARAM>no |
<SETSSLPARAM>NO |
<SETSTATE>no |
<SETSTATE>NO {
	yylval.yy_onoff = 0;
	if(debugL())
		printf("lex:YESNO(%d)\n",yylval.yy_onoff);
	return YESNO;
	}



<SETSSLPARAMDENYRENEG>yes |
<SETSSLPARAMDENYRENEG>YES |
<SETSSLPARAMDENYRENEG>no |
<SETSSLPARAMDENYRENEG>NO {
	yylval.yy_data = strdup(yytext);
	if(debugL())
		printf("lex:NAME(%s)\n",yylval.yy_data);
	return NAME;
} 



<SETSSLPARAM>enabled |
<SETSSLPARAM>ENABLED |
<SETSTATE>enabled |
<SETSTATE>ENABLED {
	yylval.yy_onoff = 1;
	if(debugL())
		printf("lex:ONOFF(%d)\n",yylval.yy_onoff);
	return ONOFF;
	}


<SETSSLPARAM>disabled |
<SETSSLPARAM>DISABLED |
<SETSTATE>disabled |
<SETSTATE>DISABLED {
	yylval.yy_onoff = 0;
	if(debugL())
		printf("lex:ONOFF(%d)\n",yylval.yy_onoff);
	return ONOFF;
	}


<SETSTATE>parameter {
		BEGIN SETSSLPARAM;
		if(debugL())
			printf("lex:(SSLPARAM)\n");
		return SSLPARAM;
	} 


<SETSTATE>-cipherRedirect      {if(debugL())printf("lex:(CIPHERDRCT)\n");return CIPHERDRCT;}
<SETSTATE>-cipherURL           {if(debugL())printf("lex:(CIPHERURL)\n");return CIPHERURL;}
<SETSTATE>-clearTextPort       {if(debugL())printf("lex:(CLRTXTPORT)\n");return CLRTXTPORT;}
<SETSTATE>-clientAuth          {if(debugL())printf("lex:(CLNTAUTH)\n");return CLNTAUTH;}
<SETSTATE>-clientCert          {if(debugL())printf("lex:(CLNTCERT)\n");return CLNTCERT;}
<SETSTATE>-dh                  {if(debugL())printf("lex:(DH)\n");return DH;}
<SETSTATE>-dhFile              {if(debugL())printf("lex:(DHFILE)\n");return DHFILE;}
<SETSTATE>-dhCount             {if(debugL())printf("lex:(DHCOUNT)\n");return DHCOUNT;}
<SETSTATE>-dhKeyExpSizeLimit   {if(debugL())printf("lex:(DHKEYEXPLIMIT)\n");return DHKEYEXPLIMIT;}
<SETSTATE>-eRSA                {if(debugL())printf("lex:(ERSA)\n");return ERSA;}
<SETSTATE>-eRSACount           {if(debugL())printf("lex:(ERSACOUNT)\n");return ERSACOUNT;}
<SETSTATE>-nonFipsCiphers      {if(debugL())printf("lex:(NONFIPSCIPHER)\n");return NONFIPSCIPHER;}
<SETSTATE>-pushEncTrigger      {if(debugL())printf("lex:(PSHENCTRG)\n");BEGIN PSHENCTRGSTATE;return PSHENCTRG;}
<SETSTATE>-redirectPortRewrite {if(debugL())printf("lex:(RDRCTPORTRW)\n");return RDRCTPORTRW;}
<SETSTATE>-sendCloseNotify     {if(debugL())printf("lex:(SNDCN)\n");return SNDCN;}
<SETSTATE>-sessReuse           {if(debugL())printf("lex:(SESSREUSE)\n");return SESSREUSE;}
<SETSTATE>-sessTimeout         {if(debugL())printf("lex:(SESSTIMEOUT)\n");return SESSTIMEOUT;}
<SETSTATE>-SNIEnable           {if(debugL())printf("lex:(SNI)\n");return SNI;}
<SETSTATE>-sslProfile          {if(debugL())printf("lex:(SSLPROF)\n");return SSLPROF;}
<SETSTATE>-dtlsProfileName     {if(debugL())printf("lex:(DTLSPROF)\n");return DTLSPROF;}
<SETSTATE>-sslRedirect         {if(debugL())printf("lex:(SSLRDRCT)\n");return SSLRDRCT;}
<SETSTATE>-sslv2Redirect       {if(debugL())printf("lex:(SSL2RDRCT)\n");return SSL2RDRCT;}
<SETSTATE>-sslv2URL            {if(debugL())printf("lex:(SSLV2URL)\n");return SSLV2URL;}
<SETSTATE>-serverAuth          {if(debugL())printf("lex:(SRVRAUTH)\n");return SRVRAUTH;}
<SETSTATE>-commonName          {if(debugL())printf("lex:(CMNNAME)\n");return CMNNAME;}

<SETSTATE>-ssl2		|
<SETSTATE>-ssl3		|
<SETSTATE>-tls1		|
<SETSTATE>-tls11	|
<SETSTATE>-tls12	{
	yylval.yy_data = strdup(yytext);
	if(debugL())
		printf("lex:SSLVERSION(%s)\n",yytext);
	return SSLVERSION;
	}

<PSHENCTRGSTATE>Always |
<PSHENCTRGSTATE>Ignore |
<PSHENCTRGSTATE>Merge  |
<PSHENCTRGSTATE>Timer  {
	BEGIN SETSTATE;
	yylval.yy_data = strdup(yytext);
	if(debugL())
		printf("lex:PSHENCTRGVAL(%s)\n",yytext);
	return PSHENCTRGVAL;
	}

<BINDSTATE>-cipherName {
	if(debugL())
		printf("lex:(CIPHERNAMETOK)\n");
	return CIPHERNAMETOK;
	}

<BINDSTATE>-eccCurveName {
	if(debugL())
		printf("lex:(ECCCURVETOK)\n");
	return ECCCURVETOK;
	}

<ADDSSLSTATE>cipher |
<BINDSTATE>cipher	{
	if(debugL())
		printf("lex:(CIPHERTOK)\n");
	return CIPHERTOK;
	}



<SETSSLPARAM>-denySSLReneg {if(debugL())printf("lex:(-denySSLReneg)\n");BEGIN SETSSLPARAMDENYRENEG;return PARAM_DENYRENEG;}
<SETSSLPARAM>-dropReqWithNoHostHeader {if(debugL())printf("lex:(-dropReqWithNoHostHeader)\n");return PARAM_DROPNOHOSTHDR;}
<SETSSLPARAM>-encryptTriggerPktCount {if(debugL())printf("lex:(-encryptTriggerPktCount)\n");return PARAM_ENCRTRIGPKTCOUNT;}
<SETSSLPARAM>-insertionEncoding {if(debugL())printf("lex:(-insertionEncoding)\n");return PARAM_INSRTENCODING;}
<SETSSLPARAM>-pushEncTriggerTimeout {if(debugL())printf("lex:(PARAM_PUSHTRIGTMOUT)\n");return PARAM_PUSHTRIGTMOUT;}
<SETSSLPARAM>-pushFlag {if(debugL())printf("lex:(-pushFlag)\n");return PARAM_PUSHFLG;}
<SETSSLPARAM>-quantumSize {if(debugL())printf("lex:(-quantumSize)\n");return PARAM_QNTMSZ;}
<SETSSLPARAM>-sendCloseNotify {if(debugL())printf("lex:(-sendCloseNotify)\n");return PARAM_SNDCLOSENTFY;}
<SETSSLPARAM>-sslTriggerTimeout {if(debugL())printf("lex:(PARAM_TRGTMOUT)\n");return PARAM_TRGTMOUT;}
<SETSSLPARAM>-strictCAChecks {if(debugL())printf("lex:(PARAM_STRCTCACHK)\n");return PARAM_STRCTCACHK;}
<SETSSLPARAM>-crlMemorySizeMB {if(debugL())printf("lex:(PARAM_CRLMEMSZ)\n");return PARAM_CRLMEMSZ;}
<SETSSLPARAM>-ocspCacheSize {if(debugL())printf("lex:(PARAM_OCSPCACHESZ)\n");return PARAM_OCSPCACHESZ;}
<SETSSLPARAM>-undefActionControl {if(debugL())printf("lex:(PARAM_UNDEFACTCTRL)\n");return PARAM_UNDEFACTCTRL;}
<SETSSLPARAM>-undefActionData {if(debugL())printf("lex:(PARAM_UNDEFACTDATA)\n");return PARAM_UNDEFACTDATA;}





[a-zA-Z0-9#_\-.:/@]+* {
	int	mod = rule_matched ? WORD : NAME;
	yylval.yy_data = strdup(yytext);
	if(debugL())
		printf("lex:%s(%s)\n",(mod==WORD)?"WORD":"NAME",yytext);
	return mod;
	}



\n  {
	BEGIN 0; 
	curstate=0;lineNo++;
	//bzero(&SetAttr,sizeof(SetAttr));
	return yytext[0];
	}
.
%%
