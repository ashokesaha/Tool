#include <stdio.h>
#include <fcntl.h>

//off_t offset = 0x07ad1ff000;
//off_t offset = 0x651d7000;
//off_t offset = 0x17550000;
off_t offset = 0x16ade000;
off_t coff = 0x01d99feee0;
off_t doff = 0x01d99ff2e0;
//off_t offset = 0x01d9a00000;
//off_t offset = 0x01d9bff800;

main()
{
	int i;
	unsigned char buf[1024];
	unsigned long long		*p64;
	int	fd = open("/dev/mem",O_RDONLY);

	lseek(fd,coff,SEEK_SET);
	read(fd,buf,1024);
	p64 = (unsigned long long *)buf;

	for(i=0;i<1;i++)
	{
		printf("%016llx\n",*p64++);
		printf("%016llx\n",*p64++);
		printf("%016llx\n",*p64++);
		printf("%016llx\n",*p64++);
		printf("\n");
	}
	printf("\n");


	lseek(fd,doff,SEEK_SET);
	read(fd,buf,1024);
	p64 = (unsigned long long *)buf;
	for(i=0;i<10;i++)
	{
		printf("%016llx\n",*p64++);
		printf("%016llx\n",*p64++);
		printf("%016llx\n",*p64++);
		printf("%016llx\n",*p64++);
		printf("\n");
	}
	printf("\n");

	return 0;
}
