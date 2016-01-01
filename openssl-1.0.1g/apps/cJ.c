#include <stdio.h>
#include <stdlib.h>
#include "cJSON.h"

main()
{
	cJSON	*root,*root2,*rA;
	char	*out;

	root	= cJSON_CreateObject();	
	cJSON_AddStringToObject(root,"key-1", "val-1");
	cJSON_AddStringToObject(root,"key-2", "val-2");
	cJSON_AddStringToObject(root,"key-3", "val-3");

	root2	= cJSON_CreateObject();	
	cJSON_AddStringToObject(root2,"key-1", "val-1");
	cJSON_AddStringToObject(root2,"key-2", "val-2");
	cJSON_AddStringToObject(root2,"key-3", "val-3");


	out	= cJSON_Print(root);
	printf("%s\n",out);
	out	= cJSON_Print(root2);
	printf("%s\n",out);

	cJSON_AddItemToObject(root,"root-2",root2);
	out	= cJSON_Print(root);
	printf("%s\n",out);


	rA = cJSON_CreateArray();

	root	= cJSON_CreateObject();	
	cJSON_AddStringToObject(root,"key-1", "val-1");
	cJSON_AddItemToArray(rA,root);

	root	= cJSON_CreateObject();	
	cJSON_AddStringToObject(root,"key-2", "val-2");
	cJSON_AddItemToArray(rA,root);

	root	= cJSON_CreateObject();	
	cJSON_AddStringToObject(root,"key-3", "val-3");
	cJSON_AddItemToArray(rA,root);

	out	= cJSON_Print(rA);
	printf("%s\n",out);
}
