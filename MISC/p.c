#include <stdio.h>

int	addVserver(int I);
int	setVProfile(int I, char *pname);

main(int argc, char **argv)
{
	addVserver(atoi(argv[1]));
	printf("sleep 5\n");
	setVProfile(atoi(argv[1]),"tmp_1");
}


int	addVserver(int I)
{
	int i;
	for (i=1;i<=I;i++)
		printf("add lb vserver  v_%d ssl 10.102.28.236 %d\n",i,1000+i);
	printf("\n");
	return 0;
}


int	setVProfile(int I, char *pname)
{
	int i;
	for (i=1;i<=I;i++)
		printf("set ssl vserver  v_%d -sslprofile %s\n",i,pname);
	printf("\n");
	return 0;
}
