#include <stdio.h>
#include <unistd.h>

main(int argc, char **argv)
{
	int		i,count = atoi(argv[1]);
	FILE 	*fp = NULL;
	char	buf[1024];

	for (i=0; i < count; i++)
	{
		usleep(1024 * 100);
	}

#if 0
	for (i=0; i < count; i++)
	{
		fp = fopen("catfile","r");
		setbuf(fp,NULL);
		fseek(fp,0,SEEK_END);
		fseek(fp,0,SEEK_SET);
		fread(buf, 257,1,fp);	
		fseek(fp,256 * 1024,SEEK_SET);
		fread(buf, 257,1,fp);	
		fseek(fp,800 * 1024,SEEK_SET);
		fread(buf, 257,1,fp);	
		fclose(fp);
	}
#endif

}
