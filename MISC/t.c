#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct _pad_map_ {
        unsigned char         *pad[256];
        unsigned char         *data;
} PAD_MAP_t;


main()
{
	PAD_MAP_t	P;
	unsigned char *ptr;
	int i,j,v=1;

	P.data = malloc(40 * 1024);
	ptr = P.data;	

	for(i=1;i<=32;i++)
    {
        for(j=1;j<=8;j++)
        {
			printf("i %d j %d v %d ptr %p\n",i,j,v,ptr);
			fflush(stdout);
            P.pad[v] = ptr;
            memset(ptr,v,i*8);
            ptr += (i * 8);
            v++;
			if(v > 255)
				break;
        }
    }
	while(1);

}
