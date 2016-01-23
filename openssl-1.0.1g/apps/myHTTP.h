#include "cJSON.h"

#define		BUFUNITSIZE		1024
#define		BUFUNITNUM		128
#define		MAXSTATUSSIZE	256	
#define		MAXHDRSIZE		4 * 1024
#define		MAXHEADERS		64	
#define		MAXBUFELEMENT	64	


#define		SP				' '
#define		CR				0x0d
#define		LF				0x0a
#define		COL				':'	

#define		STATUSOK		200
#define		STATUSCREATED	201

#define		CONTENTLEN		"Content-Length"


typedef	enum	http_resp_state {
	resp_init,
	resp_status,
	resp_header,
	resp_body,
	resp_done,
	resp_err
} RESP_state;


typedef struct _status_line_ {
	char	*version;
	char	*status;
	char 	*reason;
	int		substatus;

#define		STATUS_START	0
#define		STATUS_VER		1
#define		STATUS_CODE		2
#define		STATUS_REASN	3
#define		STATUS_CR		4
#define		STATUS_LF		5
#define		STATUS_DONE		6
} STATUS_LINE;


typedef struct _name_value_ {
	char	*name;
	char	*value;
} NAMEVAL;

typedef struct _header_ {
	int				nameValNum;
	int				curNum;
	NAMEVAL			*nameVal;
	int				substatus;
#define		HEADER_START			0
#define		HEADER_NAME_START		1
#define		HEADER_NAME				2
#define		HEADER_VAL_START		3
#define		HEADER_VAL				4
#define		HEADER_VAL_DONE			5
#define		HEADER_VAL_DONE_CR		6
#define		HEADER_DONE_CR			10
#define		HEADER_DONE_CRLF		11
} HEADER;


typedef	struct	_buf_ele_ {
	char	*ptr;
	int		len;
}BUF_ELEMENT;


typedef	struct	_http_ctx_ {
	char			*username;	
	char			*passwd;	
	char			*host;
	char			*sessid;
	int				sockfd;
	unsigned int	flags;
	cJSON			*req;
	cJSON			*res;
	BUF_ELEMENT		readBuf[BUFUNITNUM];
	int				lastOff;
	int				maxBodySize;
	int				bodyLen;
	RESP_state		rState;
	STATUS_LINE		Status;
	HEADER			Header;
} HTTP_CTX;





typedef	struct	_gen_ele_ {
	int			num;
	BUF_ELEMENT	*Elements;
}GEN_ELEMENT;


typedef struct	_header_ele_ {
	GEN_ELEMENT		Header;
	GEN_ELEMENT		Name;
	GEN_ELEMENT		Value;
} HEADER_ELEMENT;


typedef	struct	_http_resp_parse_ {
	HEADER_ELEMENT	*Header[MAXHEADERS];
	BUF_ELEMENT 	Payload[MAXBUFELEMENT];	
	int				respCode;
} HTTP_RESP_PARSE;





/************************************************************
Resp Read :

	while(true)
	{
		buf = malloc(1024);
		Enqueue(buf);
		off = 0

		while(true)
		{
			do
			{
				ret = read(sock,buf+off,1024 - off,NON_BLOCK);

			} while(ret == -1 &&  errno == EAGAIN);

			if (ret == 0)
				goto LoopDone; 

			ParseState = ParseResp(buf+off,ret);
			off += ret;

			if(off == 1024  ||  ParseState == DONE)
				break;
		}

		if(ParseState == DONE)
			break;
	};

LoopDone:

************************************************************/






#define	CHARTOCODE(c,ptr)	\
	switch(c) \
	{\
		case '!':\
		case '"':\
		case '#':\
		case '$':\
		case '%':\
		case '&':\
		case '\'':\
		case '(':\
		case ')':\
		case '*':\
		case '+':\
		case ',':\
		case '-':\
		case '/':\
		case '[':\
		case '\\':\
		case ']':\
		case '^':\
		case '_':\
		case '`':\
		case '{':\
		case '|':\
		case '}':\
		case ':':\
		case ' ': *ptr++='%';sprintf(ptr,"%02x",c);ptr += 2; break;\
		default : *ptr++ = c; break;\
	}



#define	TESTSTR \
"HTTP/1.1 201 Created\r\n\
Date: Tue, 01 Dec 2015 12:54:55 GMT\r\n\
Server: Apache\r\n\
Set-Cookie: SESSID=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; path=/\r\n\
Expires: Thu, 19 Nov 1981 08:52:00 GMT\r\n\
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0\r\n\
Pragma: no-cache\r\n\
Set-Cookie: sessionid=%23%23B679108790BBE901321EC01A998C1E3D42ADCF04EF4706B6B4F2D789D5FF34336942902B6CD94C872BFFD644A73D6B5D6567628B7B933BA2DDC78FAE17A4E5CDBF32BB6561148A044EA85DE81496D9F07DE90ACD02DFD51C82E0A1991624AF7A2BF8778C4163AFEA4CAA87ACD1C1B2AD07313014E4E091E6FFC40A1449A2; path=/nitro/v1\r\n\
Content-Length: 328\r\n\
Keep-Alive: timeout=15, max=100\r\n\
Connection: Keep-Alive\r\n\
Content-Type: application/json; charset=utf-8\r\n\r\n\
{ \"errorcode\": 0, \"message\": \"Done\", \"severity\": \"NONE\", \"sessionid\": \"##B679108790BBE901321EC01A998C1E3D42ADCF04EF4706B6B4F2D789D5FF34336942902B6CD94C872BFFD644A73D6B5D6567628B7B933BA2DDC78FAE17A4E5CDBF32BB6561148A044EA85DE81496D9F07DE90ACD02DFD51C82E0A1991624AF7A2BF8778C4163AFEA4CAA87ACD1C1B2AD07313014E4E091E6FFC40A1449A2\" }\r\n"





cJSON	*newLoginObject(char *username,char *passwd);
