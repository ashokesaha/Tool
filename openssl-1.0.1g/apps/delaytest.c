#include <stdio.h>
#include <stdlib.h>

main(int argc, char **argv)
{
	int	delay = atoi(argv[1]);

	Delay(delay);
}


int Delay(int i)
{
	FILE	*fp;
	char	c;

	while(i--)
	{
		fp = fopen("/mnt/ToolPkg/Server/delayfile.txt","r");
		setbuf(fp,NULL);
		while(!feof(fp))
		{
			fread(&c,1,1,fp);
		}
		fclose(fp);
	}
	return 0;
}
