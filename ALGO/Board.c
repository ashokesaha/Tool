#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ncurses.h>
#include <sys/time.h>

#define		ROW		32
#define		COL		24	
#define		SPACE	' '
#define		XSCALE	3
#define		YSCALE	1
#define		YOFF	2

typedef enum _dir_ {T,TR,R,DR,D,DL,L,TL,XX} DIR;

typedef struct _box_ {
	char	C;
	int		r;
	int		c;
	int		count;
	WINDOW	*W;
} BOX;

typedef  struct  _context_ {
	char	*P;
	DIR		curDir;
	BOX		*S[1024];
	int		sTop;	
} CTX;


BOX		BOARD[ROW][COL];
CTX		Context;
WINDOW	*PW;

typedef	char DTYPE[ROW][COL];

DTYPE	MYDATA		   = {
							{'a','b','c','d','e','f','g','h'},
							{'1','x','t','4','c','6','7','8'},
							{'1','2','y','b','c','6','7','8'},
							{'1','2','a','b','5','6','7','8'},
							{'1','2','3','4','c','6','7','8'},
							{'1','2','s','r','5','6','7','a'},
							{'1','2','3','4','5','6','7','b'},
							{'1','2','3','4','5','6','7','c'}
						};


char	sample[]	=	"ACGAAAGTCTGGGABCTTATAGCTACGTCGATAGCTACGTCGATAGCTACGTCGATAGCTACGTCGATAGCTACGTCGATAGCTGGTTCAAGTCAAGTTTCCATAGCTACGTATTGCAGTCGTACGATAGCTACGTCGATAGCTGTCCATTGGAATCTCGATACTGAGTACCTGAATGCTAGTCGATTCCATAGCTACGTATTGCAGTCGTACGATATAGCTACGTCGATAGCTACGGCTACGTATTGCAGCCATAGCTACGTATTGCAGTCGTACGATATAGCTACGTCGATAGCTACGGCTACGTATTGCCCATAGCTACGTATTGCAGTCGTACGATATAGCTACGTCGATAGCTACGGCTACGTATTGCCCATAGCTACGTATTGCAGTCGTACGATATAGCTACGTCGATAGCTACGGCTACGTATTGCAGCTACGTATTGCAGTCGTACGATATAGCTACGTCGATAGCTACGGCTACGTATTGCAGCCATAGAGCTACGTATTGCAGTCGTACGATATAGCTACGTCGATAGCTACGGCTACGTATTGCAGCCATAGGTATTGCCCATAGCTACGTATTGCAGTCGTACGATATAGCTACGTCGATAGCTACGGCTACGTATTGCCCATAGCTACGTATTGCAGTCGTACGATATAGCTACGTCGATAGCTACGGCTACGTATTGCAGCTACGTATTGCAGTCCTACGGCTACGTATTGCCCATAGCTACGTATTGCAGTCGTACGATATAGCTACGTCGATAGCTACGGCTACGTAGTCCTACGGCTACGTATTGCCCATAGCTACGTATTGCAGTCGTACGATATA";



BOX		*NextBox(BOX *B)
{
	int		r,c;

	r	= B->r;
	c	= B->c;

	switch(Context.curDir)
	{
		case	T : 
			r--;
			break;
		case	TR : 
			r--;
			c++;
			break;
		case	R : 
			c++;
			break;
		case	DR : 
			r++;
			c++;
			break;
		case	D : 
			r++;
			break;
		case	DL : 
			r++;
			c--;
			break;
		case	L : 
			c--;
			break;
		case	TL : 
			r--;
			c--;
			break;
	}

	if(r < 0 || r >= ROW || c < 0 || c >= COL)
		return NULL;

	return &BOARD[r][c];
}


int		MATCH()
{
	int		i,r,c;

	for(i=0; i<Context.sTop; i++)
	{
		r = Context.S[i]->r;
		c = Context.S[i]->c;

		mvaddch(r * YSCALE + YOFF, c * XSCALE,SPACE);
		wattron(PW,COLOR_PAIR(1));
		addch(BOARD[r][c].C);
		wattroff(PW,COLOR_PAIR(1));
		addch(SPACE);
	}
	wrefresh(PW);
	printf("\n");
	return 0;
}


int		StartFrom(BOX *B)
{
	DIR		d;
	int		savedTop;

	B->count++;
	if(B->C != Context.P[0])
		return 0;

	Context.S[Context.sTop++] = B;
	savedTop = Context.sTop;

	for(d=T; d<XX; d++)
	{
		Context.curDir = d;
		Context.sTop   = savedTop;

		while( (B = NextBox(Context.S[Context.sTop - 1])) )
		{
			B->count++;
			if(B->C != Context.P[Context.sTop])
				break;
			Context.S[Context.sTop++] = B;
		}

		if(Context.P[Context.sTop] == 0)
			MATCH();
	}

	Context.sTop = 0;
	return 0;
}


int		InitBoard(DTYPE DATA)
{
	int		r,c;
	
	for(r=0; r<ROW; r++)
		for(c=0; c<COL; c++)
		{
			BOARD[r][c].C = DATA[r][c];
			BOARD[r][c].r = r;
			BOARD[r][c].c = c;
			BOARD[r][c].count = 0;
		}
	return 0;
}


int		InitContext(char *p)
{
	Context.P		= p;
	Context.sTop	= 0;
	Context.curDir	= T;
	return 0;
}


int		InitCurses()
{
	PW = initscr();
	start_color();
	init_pair(1, COLOR_BLACK, COLOR_WHITE);
}


int		WriteData()
{
	int		r,c;

	for(r=0; r<ROW; r++)
	{
		for(c=0; c<COL; c++)
		{
			mvaddch(r * YSCALE + YOFF, c * XSCALE,SPACE);
			addch(BOARD[r][c].C);
			addch(SPACE);
		}
	}
	refresh();
	return 0;
}


int		Str2Data(char *str)
{
	int		r,c;

	memset((unsigned char *)MYDATA,'.', sizeof(MYDATA));

	if(!*str)
		return 0;

	for(r=0; r<ROW; r++)
		for(c=0; c<COL; c++)
		{
			MYDATA[r][c] = *str++;
			if(MYDATA[r][c] == SPACE)
				MYDATA[r][c] = 'a';
			if(!*str)
				break;
		}
	return 0;
}


int		BoardWeight()
{
	int		r,c, w=0;
	
	for(r=0; r<ROW; r++)
	{
		for(c=0; c<COL; c++)
		{
			w += BOARD[r][c].count;
			printf("%02d ",BOARD[r][c].count);
		}
		printf("\n");
	}
	printf("Total Weight : %d\n",w);
	return 0;
}


int		Shuffle(char *p,int iter)
{
	int		i,l,r1,r2,t;

	printf("\n\n");
	printf("----------------------------------------------\n");
	l = strlen(p);

	for(i=0;i<l;i++)
		if((p[i] =='C') || (p[i] =='G'))
			p[i] = (i%2) ? 'A' : 'B';

	for(i=0;i<l;i++)
		if(p[i] =='T')
			p[i] = ((i==0) ? 'T' : ((i==1) ? 'A' : 'B'));

	for(i=0; i<iter; i++)
	{
		r1	= random() % l;
		r2	= random() % l;
		t	= p[r1];
		p[r1] = p[r2];
		p[r2] = t;
	}
	return 0;
}


int		InitRandom()
{
	struct timeval	tv;

	gettimeofday(&tv,NULL);
	srandom(tv.tv_usec);
	return 0;
}


main(int argc, char **argv)
{
	int		r,c;

	InitRandom();
	InitContext(argv[1]);
	Shuffle(sample,500);
	Str2Data(sample);
	InitBoard(MYDATA);

	InitCurses();
	WriteData();

	for(r=0; r<ROW; r++)
		for(c=0; c<COL; c++)
			StartFrom(&BOARD[r][c]);

	endwin();
	BoardWeight();
}
