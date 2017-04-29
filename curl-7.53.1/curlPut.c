#include <stdio.h>
#include <strings.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "curl/curl.h"


static size_t read_callback(void *ptr, size_t size, size_t nmemb, void *stream)
{
	char buf[] =	"0123456789012345678901234567890123456789\
					 0123456789012345678901234567890123456789\
					 0123456789012345678901234567890123456789" ;
					
	if(size >= 64)
		return 0;

	printf("read_callback : size %d\n", size);
	bcopy(&buf[size],ptr,8);
	return 8;
}



main()
{
	CURL		*curl;
	CURLcode	res;

	curl = curl_easy_init();
	curl_easy_setopt(curl, CURLOPT_READFUNCTION, read_callback);
	curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);
	curl_easy_setopt(curl, CURLOPT_PUT, 1L);
	curl_easy_setopt(curl, CURLOPT_URL, "http://10.102.28.61:8080/");
	curl_easy_setopt(curl, CURLOPT_INFILESIZE_LARGE,64);
	res = curl_easy_perform(curl);

	if(res != CURLE_OK)
		printf("curl_easy_perform() failed: %s\n",curl_easy_strerror(res));
 
    curl_easy_cleanup(curl);
}
