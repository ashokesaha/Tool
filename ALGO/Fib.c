#include <stdio.h>
#include <stdlib.h>

int	N[1024] = {0};

int	Fib(int n)
{
	N[n]++;

	if(n == 0)	return 0;
	if(n == 1)	return 0;
	if(n == 2)	return 1;
	return Fib(n-2) + Fib(n-1);
}


int	Fib2(n)
{
	int	F[1024];
	int	top = 0;

	F[top++] = Fib(0);
	F[top++] = Fib(1);
	F[top++] = Fib(2);

	for(;top <= n; top++)
		F[top] = F[top - 1] + F[top - 2];

	top--;
	printf("Fib(%d): %d\n",top,F[top]);
	return 0;
}


main(int argc, char **argv)
{
	int		n;
	
	n = Fib(atoi(argv[1]));
	printf("Fib(%d) = %d\n",atoi(argv[1]),n);
	for(n=0; n<=atoi(argv[1]);n++)
		printf("Fib(%02d) : %d\n", n,N[n]);
	printf("\n");

	//Fib2(atoi(argv[1]));
}
