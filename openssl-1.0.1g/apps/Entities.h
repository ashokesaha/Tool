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


#define	ADDLBVSERVER	\
"object={\"lbvserver\":{\"name\":\"%s\",\"servicetype\":\"%s\",\"ipv46\":\"%s\",\"port\":\"%d\"}}"

#define	ADDSERVERCERT	\
"object={\"sslcertkey\":{\"certkey\":\"%s\",\"cert\":\"%s\",\"key\":\"%s\"}}"
