#include <stdio.h>
main(int argc,char **argv)
{
	int i;

	for(i=1;i<atoi(argv[1]);i++)	
		printf("%03d\n",i);
}
