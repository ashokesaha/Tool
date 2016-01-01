#define		ROW			8
#define 	COL			8
#define		CELLH		2
#define		CELLW		4
#define		XMARGIN		4
#define		YMARGIN		2
#define		MAXSTACK	1024

typedef enum _dir_ {
	D, DL, L, TL, T, TR, R, DR, DXX } DIR;


typedef struct _nxt_ {
	bool D[DXX];
	int		cur;
} NXT;


typedef struct _E_ {
	char	C;
	int		pos;
	NXT		N;
	int		nxt;
	bool	pushed;	

	int		attr;
	WINDOW	*W;
} E;


typedef struct _estack_ {
	E	*S[MAXSTACK];
	int	top;
} ESTACK;



int		PUSH(E *e);
E		*POP();
E		*TOP();
int		ISSTACKEMPTY();
int		RunFrom(E	*e);
int		NEWPOS(E *e, int pos);
DIR		getNextDir(E *e);
E		*getNextE(E *e);
int		ON(E *e);
int		OFF(E *e);
int		DONE();
int		getRowCol(E *e, int *r, int *c);
E		*getT(E *e);
E		*getD(E *e);
E		*getL(E *e);
E		*getR(E *e);
E		*getTL(E *e);
E		*getTR(E *e);
E		*getDL(E *e);
E		*getDR(E *e);
int		initM(char a[ROW][COL]);
int		refreshM();
int		drawE(E *e,int r, int c);
int		drawM();
