#include "myHTTP.h"
#include "hashdef.h"
#include "cJSON.h"

cJSON	*ReadResponse(HTTP_CTX *ctx);
cJSON	*newVserverObject(HTTP_CTX *,char *,char *,int ,char *);
cJSON	*javaLogin(char *username,char *passwd);
cJSON	*javaAddHTTPVserver(char *vservername,char *ip,int port);
cJSON	*javaAddSSLVserver(char *vservername,char *ip,int port);
cJSON	*javaDelVserver(char *vservername);
cJSON	*javaAddHTTPService(char *service,char *server,int port);
cJSON	*javaDelHTTPService(char *service);
cJSON	*javaAddSSLService(char *service,char *server,int port);
cJSON	*javaDelSSLService(char *service);
cJSON	*javaAddServer(char *servername,char *ip);
cJSON	*javaDelServer(char *servername);
cJSON	*javaAddCertKey(char *,char *,char *);
cJSON	*javaDelCertKey(char *);
cJSON	*javaBindUnbindCertKey(char *,char *,int,int , int , int );


int		jsonSendRecv(cJSON *json,int sock);

