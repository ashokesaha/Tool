#include <stdio.h>

char	*caname[] =
{
"BANGALORECA",
"BHOPALCA",
"CALCUTTACA",
"CHENNAICA",
"DELHICA",
"GOACA",
"KOCHICA",
"MUMBAICA",
"MYSORECA",
"OOTYCA",
"PATNACA",
"RANCHICA",
"SHILLONGCA",
NULL
};



main()
{
	int	i,j;

	for(i=0;caname[i];i++)
	{
		for(j=1; j<= 140; j++)
		{
			printf("10.102.28.61		%03d_%s\n", j, caname[i]);
		}
	}


}
