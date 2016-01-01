#include <stdio.h>
#include <stdlib.h>
#include <ncurses.h>
#include "cursestest.h"




WINDOW *PW = NULL;
int		wX = 0, wY = 0, Pos = 0;
E		M[ROW][COL];
ESTACK	STK;
char	*PTRN = "1232";
FILE	*logfp = NULL;


int		PUSH(E *e)
{
	if(STK.top >= MAXSTACK)
		return -1;

	e->pos = Pos;

	STK.S[STK.top++] = e;
	e->pushed = TRUE;
	ON(e);
	return 0;
}

E	*POP()
{
	E *e;
	
	if(STK.top == 0)
		return NULL;
	STK.top--;
	e = STK.S[STK.top];
	STK.S[STK.top] = NULL;
	clearE(e);
	OFF(e);
	return e;
}


E	*TOP()
{
	return STK.S[STK.top];
}


int	ISSTACKEMPTY()
{
	if(STK.top == 0)
		return 1;
	return 0;
}


int	RunFrom(E	*e)
{
	int	 dd=1;
	E	*eT;


	if(e->C != PTRN[Pos])
		return 0;

	PUSH(e);
	Pos++;

	while(!ISSTACKEMPTY())
	{
		int x,y;
		while(eT = getNextE(e))
		{
			getRowCol(eT,&x,&y);
			fprintf(logfp,"			getNext (%d %d) [%c] pushed %d ", x,y, eT->C,eT->pushed);
			if(eT->pushed)
			{
				fprintf(logfp,"\n");
				continue;
			}

			if(eT->C == PTRN[Pos])
			{
				fprintf(logfp," PUSH");
				PUSH(eT);
				Pos++;
				if(PTRN[Pos] == 0)
				{
					fprintf(logfp,"\n");
					DONE();
					break;
				}
				e = eT;
				fprintf(logfp,"		New Anchor (%d %d) [%c] pushed %d ", x,y, eT->C,eT->pushed);
			}
			fprintf(logfp,"\n");
		}

		if(ISSTACKEMPTY())
			break;
		e = POP();

		getRowCol(e,&x,&y);
		fprintf(logfp,"		POP (%d %d) [%c] \n", x,y, e->C);

		Pos = e->pos;
	}
}


int	NEWPOS(E *e, int pos)
{
	int		i,j;

	e->pos = pos;
	for(i=0; i<DXX;i++)
		e->N.D[i] = TRUE;

	getRowCol(e,&i,&j);

	if(i==0)
	{
		e->N.D[T] = FALSE;
		e->N.D[TR] = FALSE;
		e->N.D[TL] = FALSE;
	}
	else if(i==ROW-1)
	{
		e->N.D[D] = FALSE;
		e->N.D[DR] = FALSE;
		e->N.D[DL] = FALSE;
	}

	if(j==0)
	{
		e->N.D[L] = FALSE;
		e->N.D[TL] = FALSE;
		e->N.D[DL] = FALSE;
	}
	else if(j==COL-1)
	{
		e->N.D[R] = FALSE;
		e->N.D[TR] = FALSE;
		e->N.D[DR] = FALSE;
	}


	return 0;
}

DIR	getNextDir(E *e)
{
	DIR D = DXX,DT;	
	int	x,y;
	while(e->N.cur < DXX)
	{
		getRowCol(e,&x,&y);
		fprintf(logfp,"		getNextDir (%d %d) [%c] cur %d (%d)\n", x,y, e->C,e->N.cur, e->N.D[e->N.cur]);
		if(e->N.D[e->N.cur])
		{
			e->N.D[e->N.cur] = FALSE;
			D = e->N.cur;
			e->N.cur++;
			break;
		}
		e->N.cur++;
	}
	return D;
}


E	*getNextE(E *e)
{
	int		i,j,n;
	E		*eT = NULL;
	DIR		d;


	
	while((d = getNextDir(e)) != DXX)
	{
	getRowCol(e,&i,&j);

	switch(d)
	{
		case D:	
			i++;
			break;
		case DL:	
			i++;
			j--;
			break;
		case L:	
			j--;
			break;
		case TL:	
			i--;
			j--;
			break;
		case T:	
			i--;
			break;
		case TR:	
			i--;
			j++;
			break;
		case R:	
			j++;
			break;
		case DR:	
			i++;
			j++;
			break;
	}

	if( i<0 || i>=COL || j<0  ||  j >= ROW)
		continue;
	else
		break;
	}

	if(d == DXX)
		return NULL;

	eT = &M[i][j];
	return eT;
}


int	ON(E *e)
{
	wattron(e->W,e->attr);
	mvwaddch(e->W,1,1,e->C);
	waddch(e->W, ' ');
	wrefresh(e->W);
}

int	OFF(E *e)
{
	wattroff(e->W,e->attr);
	mvwaddch(e->W,1,1,e->C);
	waddch(e->W, ' ');
	wrefresh(e->W);
}

int	DONE()
{
	int	i;
	int	x,y;

	for(i=0;i<STK.top;i++)
	{
		//wattron((STK.S[i])->W,A_BLINK);
		//mvwaddch((STK.S[i])->W,1,1,' ');
		//waddch((STK.S[i])->W, ' ');
		//wrefresh((STK.S[i])->W);

		getRowCol(STK.S[i],&y,&x);
		fprintf(logfp,"(%d %d) ",y,x);
		clearE(STK.S[i]);
		STK.S[i] = NULL;
	}
	fprintf(logfp,"\n");
	STK.top = 0;
	Pos = 0;
	return 0;
}


int	clearE(E *e)
{
	DIR d;
	e->pos = 0;
	e->pushed = FALSE;
	for(d=0;d < DXX; d++)
		e->N.D[d] = TRUE;
	return 0;
}

int	getRowCol(E *e, int *r, int *c)
{
	int	i,j,n;

	n = ((unsigned int)e - (unsigned int)(&M[0][0]))/sizeof(E);
	i = n/ROW;
	j = n%COL;

	*r = i;
	*c = j;

	return 0;
}


E	*getT(E *e)
{
	int	i,j;

	getRowCol(e,&i,&j);
	if(i == 0)
		return NULL;
	i--;
	return &M[i][j];
}

E	*getD(E *e)
{
	int	i,j;

	getRowCol(e,&i,&j);
	if(i == (ROW - 1))
		return NULL;
	i++;
	return &M[i][j];
}

E	*getL(E *e)
{
	int	i,j;

	getRowCol(e,&i,&j);
	if(j == 0)
		return NULL;
	j--;
	return &M[i][j];
}

E	*getR(E *e)
{
	int	i,j;

	getRowCol(e,&i,&j);
	if(j == (COLS - 1)) 
		return NULL;
	j++;
	return &M[i][j];
}

E	*getTL(E *e)
{
	int	i,j;

	getRowCol(e,&i,&j);
	if(j == (COLS - 1)) 
		return NULL;
	if(i == 0) 
		return NULL;
	i--;
	j--;
	return &M[i][j];
}

E	*getTR(E *e)
{
	int	i,j;

	getRowCol(e,&i,&j);
	if(j == (COLS - 1)) 
		return NULL;
	if(i == (COLS - 1)) 
		return NULL;
	i--;
	j++;
	return &M[i][j];
}

E	*getDL(E *e)
{
	int	i,j;

	getRowCol(e,&i,&j);
	if(i == (ROW - 1)) 
		return NULL;
	if(j == 0) 
		return NULL;
	i++;
	j--;
	return &M[i][j];
}

E	*getDR(E *e)
{
	int	i,j;

	getRowCol(e,&i,&j);
	if(i == (ROW - 1)) 
		return NULL;
	if(j == (COLS - 1)) 
		return NULL;
	i++;
	j++;
	return &M[i][j];
}

int	initM(char a[ROW][COL])
{
	int i,j;
	DIR	D;

	init_pair(1,COLOR_BLACK,COLOR_WHITE);

	
	for(i=0;i<ROW;i++)
	{
		for(j=0;j<COL;j++)
		{
			M[i][j].C		= a[i][j];

			for(D=0; D<DXX; D++)
				M[i][j].N.D[D]	= TRUE;
			M[i][j].N.cur	= 0;
			M[i][j].pos		= 0;

			M[i][j].W		= derwin(PW,1+(CELLH),1+(CELLW),i*CELLH + YMARGIN,j*CELLW + XMARGIN);
			M[i][j].attr	= COLOR_PAIR(1); 
		}
	}

	return 0;
}


int	refreshM()
{
	refresh();
	return 0;
}



int	drawE(E *e,int r, int c)
{
	wborder(e->W, '|', '|', '-', '-', '*', '*', '*', '*');
	mvwaddch(e->W,1,1,e->C);
	wrefresh(e->W);
	refresh();
	return 0;
}


int drawM()
{
	int i,j;
	for(i=0;i<ROW;i++)
	{
		for(j=0;j<COL;j++)
		{
			drawE(&M[i][j],i,j);
		}
	}

	return 0;
}



int main()
{
	int		x,y;
	int		i,j;
	char	A[ROW][COL] =	{
								{'1','2','3','4','5','6','7','8'},	
								{'9','0','1','2','3','4','5','6'},	
								{'7','8','9','0','1','2','3','4'},	
								{'5','6','7','8','9','0','1','2'},	
								{'3','4','5','6','7','8','9','0'},	
								{'1','2','3','4','5','6','7','8'},	
								{'9','0','1','2','3','4','5','6'},	
								{'7','8','9','0','1','2','3','4'}
							};
	int dd = 1;

	logfp = fopen("log.out","w");
	setbuf(logfp,NULL);

	PW = initscr();
	refresh();

	if(has_colors() == FALSE)
	{
		printf("Your terminal does not support color\n");
		exit(1);
	}

	start_color();

	getmaxyx(PW,wY,wX);

	x = wX;
	y = wY * 2;

	if(x > y)
		x = y;
	else
		y = x;	

	x  -= 8;
	y  -= 4;

	y = y/2;

	initM(A);
	drawM();


#if 0

	for(i=0, j=0; i < ROW; i++)
	{
		M[i][j].N.D[L] = FALSE;
		M[i][j].N.D[TL] = FALSE;
		M[i][j].N.D[DL] = FALSE;
	}
	for(i=0, j=COL-1; i < ROW; i++)
	{
		M[i][j].N.D[R] = FALSE;
		M[i][j].N.D[TR] = FALSE;
		M[i][j].N.D[DR] = FALSE;
	}
	for(i=0, j=0; j < COL; j++)
	{
		M[i][j].N.D[T] = FALSE;
		M[i][j].N.D[TL] = FALSE;
		M[i][j].N.D[TR] = FALSE;
	}
	for(i=ROW-1, j=0; j < COL; j++)
	{
		M[i][j].N.D[D] = FALSE;
		M[i][j].N.D[DL] = FALSE;
		M[i][j].N.D[DR] = FALSE;
	}
#endif

	//while(dd);

	for(i=0; i<ROW; i++)
	{
		for(j=0; j<COL; j++)
		{
			fprintf(logfp, "RunFrom (%d %d) [%c] : Pos %d\n", i,j,M[i][j].C,Pos);
			RunFrom(&M[i][j]);
		}
	}

	sleep(1000);
	endwin();			/* End curses mode		  */
	return 0;
}
