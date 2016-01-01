#include <stdio.h>
#include <unistd.h>

typedef	int (*APTR)[4][3][2]; 

main()
{
	int		i;
	APTR	A;	
	int		**AA;
	int	B[24] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24};

	A = (APTR)B;
	
	printf("%d %d %d\n%d %d %d\n",A[0][0],A[0][1],A[0][2],A[1][0],A[1][1],A[1][2]);

	printf("\\n: %d\n",'\n');
	printf("\\r: %d\n",'\r');

	for(i=0;i<100;i++)
		usleep(1 );
}
