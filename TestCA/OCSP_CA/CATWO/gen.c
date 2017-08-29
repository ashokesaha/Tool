#include <stdio.h>

main(int argc, char **argv)
{
	int	i,count;
	count = atoi(argv[1]);

	for(i=1;i<count;i++)
		printf("add certkey ocspcatwo_%03d_cert -cert /nsconfig/ssl/CATWO/ocspcatwo_%03d_cert.pem -key /nsconfig/ssl/CATWO/ocspcatwo_%03d_key.pem\n",i,i,i);

	
	/**
	for(i=1;i<count;i++)
		printf("bind ssl vserver v1 -certkeyName  ocspcatwo_%03d_cert -SNICert\n",i);
	for(i=1;i<count;i++)
		printf("bind ssl vserver v2 -certkeyName  ocspcatwo_%03d_cert -SNICert\n",i);
	**/



}
