#include <stdio.h>

main()
{
	int	c;
	unsigned char b;
	int	i = 0;
	FILE *fp = fopen("N3.out","r");	

	while((c = fgetc(fp)) >= 0)
	{
		if(i % 12  == 0) printf("\n");
		b = (unsigned char ) (c & 0x000000ff);	
		printf("0x%02x, ",b);
		i++;
	}
	printf("\n");
}
