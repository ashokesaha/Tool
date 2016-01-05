#include "cJSON.h"


typedef	struct	_http_ctx_ {
	char			*username;	
	char			*passwd;	
	char			*host;
	char			*sessid;
	int				sockfd;
	unsigned int	flags;
	cJSON			*req;
	cJSON			*res;
} HTTP_CTX;






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
		case ' ': *ptr++='%';sprintf(ptr,"%02x",c);ptr += 2; break;\
		default : *ptr++ = c; break;\
	}



#define	LOGINSTR	\
"POST /nitro/v1/config/ HTTP/1.1\r\n\
Content-Type: application/x-www-form-urlencoded\r\n\
Cache-Control: no-cache\r\n\
Pragma: no-cache\r\n\
User-Agent: Ashoke-Tool/0.9\r\n\
Host: %s\r\n\
Accept: text/html\r\n\
Connection: keep-alive\r\n\
Content-Length: %d\r\n\r\n"




cJSON	*newLoginObject(char *username,char *passwd);
