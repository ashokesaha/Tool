#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "cJSON.h"

char 	*ptr = "{\"ip\": \"192.168.10.1\", \"peerlist\": [\"one\", \"two\"], \"port\": 5050}";

main()
{
	cJSON	*cJ, *cJc;

	cJ      = cJSON_Parse(ptr);
	if(!cJ)
	{
		printf("Json parse failed\n");
		exit(0);
	}
	cJc = cJ->child;
	while(cJc)
	{
		printf("%s %d\n", cJc->string, cJc->type);
		if(cJc->type == cJSON_Array)
		{
			int i,num = cJSON_GetArraySize(cJc);
			cJSON *cjx;
			printf("Array size %d\n",num);
			for(i=0; i<num; i++)
			{
				cjx = cJSON_GetArrayItem(cJc,i);
				printf("	%s\n", cjx->valuestring);	
			}
		}
		cJc = cJc->next;
	}
}
