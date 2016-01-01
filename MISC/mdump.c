#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <fcntl.h>
#include <unistd.h>


main(int argc,char **argv)
{
	unsigned long long ll = 0;
	int	fd;	
	unsigned char buf[1024];

	ll = strtoll(argv[1],NULL,16);
	fd = open("/dev/mem",O_RDONLY);
	if(fd <= 0)
	{
		printf("/dev/mem open failed\n");
		exit(0);
	}
	if(lseek(fd,ll,SEEK_SET) <= 0)
	{
		printf("lseek  failed\n");
		exit(0);
	}
	if(read(fd,buf,atoi(argv[2])) <= 0)
	{
		printf("read failed for %d bytes \n",atoi(argv[1]));
		exit(0);
	}
	close(fd);
	for(fd=0;fd<atoi(argv[2]);fd++)
		printf("%02x ",buf[fd]);
	printf("\n");
}
