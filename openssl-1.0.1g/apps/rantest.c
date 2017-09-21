#include <stdio.h>
#include <stdlib.h>

main()
{
	int	i;
	unsigned long L[1000];
	srandomdev();

	for(i=0; i<1000; i++)
		L[i] = random();

	for(i=0; i<1000; i++)
		printf("%08x\n", L[i]);
}
