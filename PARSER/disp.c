#include <stdlib.h>
#include <string.h>
#include <ncurses.h>


typedef struct _scrollwindow_ {
	int		count;
	int		max;
	int		start;
	int		stop;
	char	**names;
	WINDOW	*win;
} SCROLLWINDOW;


WINDOW		*AddScrollWindow();
WINDOW		*AddPromptWindow(char *);
int			DelPromptWindow(WINDOW *);
int			keyPress(SCROLLWINDOW *win);
int			SCROLLWINDOW_print(SCROLLWINDOW *scw);
char 		**createNames(int count);


#define		MAXNAMES	50
#define		TOPBORDER	3
#define		BTMBORDER	5

main()
{
	WINDOW	*win = NULL;
	SCROLLWINDOW   scw;
	int	y,x;
	int	py,px;
	char	*Header = "Batch Generator";

	initscr();
	cbreak();
	keypad(stdscr, TRUE);

	getmaxyx(stdscr,y,x);
	wborder(stdscr, '|', '|', '+','+','X','X','X','X');
	mvwhline(stdscr,TOPBORDER-1,0,'-',x);
	mvwprintw(stdscr,1,(x - strlen(Header))/2,"%s",Header);
	refresh();

	win = AddPromptWindow("what is your name:");

	bzero(&scw,sizeof(scw));
	scw.names = createNames(MAXNAMES);
	scw.max = MAXNAMES;
	scw.count = MAXNAMES;
	scw.start = 0;
	scw.stop = y - (TOPBORDER + BTMBORDER);
	scw.win = stdscr;

	keyPress(&scw);

	//SCROLLWINDOW_print(&scw);

	//scw = AddScrollWindow();
	//getch();
	//DelPromptWindow(win);
	//wscrl(scw,1);
	//getch();
	//wscrl(scw,1);

	getch();
	endwin();
}



WINDOW *AddPromptWindow(char *prompt)
{
	WINDOW	*win = NULL;
	int		y,x;

	getmaxyx(stdscr,y,x);
	win = derwin(stdscr,BTMBORDER-1,x,y-BTMBORDER+1,0);
	wborder(win, '#', '#', '=','=','#','#','#','#');
	mvwprintw(win,1,2,"%s",prompt);
	wmove(win,2,2);
	wrefresh(win);
	return win;
}


int		DelPromptWindow(WINDOW *win)
{
	int		y,x,i;

	getmaxyx(win,y,x);
	for(i=0;i<y;i++)
		mvwhline(win,i,1,' ',x);
	wrefresh(win);
	delwin(win);

	wborder(stdscr, '|', '|', '+','+','X','X','X','X');
	return 0;
}



WINDOW		*AddScrollWindow()
{
	WINDOW	*win = NULL;
	int		y,x;

	getmaxyx(stdscr,y,x);
	win = derwin(stdscr,4,6,4,6);
	wborder(win, '#', '#', '=','=','#','#','#','#');

	mvwprintw(win,1,1,"one");
	mvwprintw(win,2,1,"two");
	mvwprintw(win,3,1,"three");
	mvwprintw(win,4,1,"four");
	mvwprintw(win,5,1,"five");
	mvwprintw(win,6,1,"six");

	wrefresh(win);
	scrollok(win,1);

	return win;
}



int		keyPress(SCROLLWINDOW *scw)
{
	int	ch;
	WINDOW	*win = scw->win;

	while(ch = wgetch(win))
	{
	switch(ch)
	{
		case KEY_UP : 
			if(scw->start > 0) 
			{          
				scw->start--;
				scw->stop--;
				SCROLLWINDOW_print(scw);
			}
			break;

		case KEY_DOWN : 
			if(scw->stop < scw->count) 
			{          
				scw->start++;
				scw->stop++;
				SCROLLWINDOW_print(scw);
			}
			break;

		case KEY_LEFT : mvwprintw(win,6,10,"key KEY_LEFT\n");break;
		case KEY_RIGHT : mvwprintw(win,6,10,"key KEY_RIGHT\n");break;
		case KEY_HOME : mvwprintw(win,6,10,"key KEY_HOME\n");break;
		case KEY_BACKSPACE : mvwprintw(win,6,10,"key KEY_BACKSPACE\n");break;
		case KEY_F0 : mvwprintw(win,6,10,"key KEY_F0\n");break;
		//case KEY_F(n) : mvwprintw(win,6,10,"key KEY_F(n)\n");break;
		case KEY_DL : mvwprintw(win,6,10,"key KEY_DL\n");break;
		case KEY_IL : mvwprintw(win,6,10,"key KEY_IL\n");break;
		case KEY_DC : mvwprintw(win,6,10,"key KEY_DC\n");break;
		case KEY_IC : mvwprintw(win,6,10,"key KEY_IC\n");break;
		case KEY_EIC : mvwprintw(win,6,10,"key KEY_EIC\n");break;
		case KEY_CLEAR : mvwprintw(win,6,10,"key KEY_CLEAR\n");break;
		case KEY_EOS : mvwprintw(win,6,10,"key KEY_EOS\n");break;
		case KEY_EOL : mvwprintw(win,6,10,"key KEY_EOL\n");break;
		case KEY_SF : mvwprintw(win,6,10,"key KEY_SF\n");break;
		case KEY_SR : mvwprintw(win,6,10,"key KEY_SR\n");break;
		case KEY_NPAGE : mvwprintw(win,6,10,"key KEY_NPAGE\n");break;
		case KEY_PPAGE : mvwprintw(win,6,10,"key KEY_PPAGE\n");break;
		case KEY_STAB : mvwprintw(win,6,10,"key KEY_STAB\n");break;
		case KEY_CTAB : mvwprintw(win,6,10,"key KEY_CTAB\n");break;
		case KEY_CATAB : mvwprintw(win,6,10,"key KEY_CATAB\n");break;
		case KEY_ENTER : mvwprintw(win,6,10,"key KEY_ENTER\n");break;
		case KEY_PRINT : mvwprintw(win,6,10,"key KEY_PRINT\n");break;
		case KEY_LL : mvwprintw(win,6,10,"key KEY_LL\n");break;
		case KEY_A1 : mvwprintw(win,6,10,"key KEY_A1\n");break;
		case KEY_A3 : mvwprintw(win,6,10,"key KEY_A3\n");break;
		case KEY_B2 : mvwprintw(win,6,10,"key KEY_B2\n");break;
		case KEY_C1 : mvwprintw(win,6,10,"key KEY_C1\n");break;
		case KEY_C3 : mvwprintw(win,6,10,"key KEY_C3\n");break;
		case KEY_BTAB : mvwprintw(win,6,10,"key KEY_BTAB\n");break;
		case KEY_BEG : mvwprintw(win,6,10,"key KEY_BEG\n");break;
		case KEY_CANCEL : mvwprintw(win,6,10,"key KEY_CANCEL\n");break;
		case KEY_CLOSE : mvwprintw(win,6,10,"key KEY_CLOSE\n");break;
		case KEY_COMMAND : mvwprintw(win,6,10,"key KEY_COMMAND\n");break;
		case KEY_COPY : mvwprintw(win,6,10,"key KEY_COPY\n");break;
		case KEY_CREATE : mvwprintw(win,6,10,"key KEY_CREATE\n");break;
		case KEY_END : mvwprintw(win,6,10,"key KEY_END\n");break;
		case KEY_EXIT : mvwprintw(win,6,10,"key KEY_EXIT\n");break;
		case KEY_FIND : mvwprintw(win,6,10,"key KEY_FIND\n");break;
		case KEY_HELP : mvwprintw(win,6,10,"key KEY_HELP\n");break;
		case KEY_MARK : mvwprintw(win,6,10,"key KEY_MARK\n");break;
		case KEY_MESSAGE : mvwprintw(win,6,10,"key KEY_MESSAGE\n");break;
		case KEY_MOVE : mvwprintw(win,6,10,"key KEY_MOVE\n");break;
		case KEY_NEXT : mvwprintw(win,6,10,"key KEY_NEXT\n");break;
		case KEY_OPEN : mvwprintw(win,6,10,"key KEY_OPEN\n");break;
		case KEY_OPTIONS : mvwprintw(win,6,10,"key KEY_OPTIONS\n");break;
		case KEY_PREVIOUS : mvwprintw(win,6,10,"key KEY_PREVIOUS\n");break;
		case KEY_REDO : mvwprintw(win,6,10,"key KEY_REDO\n");break;
		case KEY_REFERENCE : mvwprintw(win,6,10,"key KEY_REFERENCE\n");break;
		case KEY_REFRESH : mvwprintw(win,6,10,"key KEY_REFRESH\n");break;
		case KEY_REPLACE : mvwprintw(win,6,10,"key KEY_REPLACE\n");break;
		case KEY_RESTART : mvwprintw(win,6,10,"key KEY_RESTART\n");break;
		case KEY_RESUME : mvwprintw(win,6,10,"key KEY_RESUME\n");break;
		case KEY_SAVE : mvwprintw(win,6,10,"key KEY_SAVE\n");break;
		case KEY_SBEG : mvwprintw(win,6,10,"key KEY_SBEG\n");break;
		case KEY_SCANCEL : mvwprintw(win,6,10,"key KEY_SCANCEL\n");break;
		case KEY_SCOMMAND : mvwprintw(win,6,10,"key KEY_SCOMMAND\n");break;
		case KEY_SCOPY : mvwprintw(win,6,10,"key KEY_SCOPY\n");break;
		case KEY_SCREATE : mvwprintw(win,6,10,"key KEY_SCREATE\n");break;
		case KEY_SDC : mvwprintw(win,6,10,"key KEY_SDC\n");break;
		case KEY_SDL : mvwprintw(win,6,10,"key KEY_SDL\n");break;
		case KEY_SELECT : mvwprintw(win,6,10,"key KEY_SELECT\n");break;
		case KEY_SEND : mvwprintw(win,6,10,"key KEY_SEND\n");break;
		case KEY_SEOL : mvwprintw(win,6,10,"key KEY_SEOL\n");break;
		case KEY_SEXIT : mvwprintw(win,6,10,"key KEY_SEXIT\n");break;
		case KEY_SFIND : mvwprintw(win,6,10,"key KEY_SFIND\n");break;
		case KEY_SHELP : mvwprintw(win,6,10,"key KEY_SHELP\n");break;
		case KEY_SHOME : mvwprintw(win,6,10,"key KEY_SHOME\n");break;
		case KEY_SIC : mvwprintw(win,6,10,"key KEY_SIC\n");break;
		case KEY_SLEFT : mvwprintw(win,6,10,"key KEY_SLEFT\n");break;
		case KEY_SMESSAGE : mvwprintw(win,6,10,"key KEY_SMESSAGE\n");break;
		case KEY_SMOVE : mvwprintw(win,6,10,"key KEY_SMOVE\n");break;
		case KEY_SNEXT : mvwprintw(win,6,10,"key KEY_SNEXT\n");break;
		case KEY_SOPTIONS : mvwprintw(win,6,10,"key KEY_SOPTIONS\n");break;
		case KEY_SPREVIOUS : mvwprintw(win,6,10,"key KEY_SPREVIOUS\n");break;
		case KEY_SPRINT : mvwprintw(win,6,10,"key KEY_SPRINT\n");break;
		case KEY_SREDO : mvwprintw(win,6,10,"key KEY_SREDO\n");break;
		case KEY_SREPLACE : mvwprintw(win,6,10,"key KEY_SREPLACE\n");break;
		case KEY_SRIGHT : mvwprintw(win,6,10,"key KEY_SRIGHT\n");break;
		case KEY_SRSUME : mvwprintw(win,6,10,"key KEY_SRSUME\n");break;
		case KEY_SSAVE : mvwprintw(win,6,10,"key KEY_SSAVE\n");break;
		case KEY_SSUSPEND : mvwprintw(win,6,10,"key KEY_SSUSPEND\n");break;
		case KEY_SUNDO : mvwprintw(win,6,10,"key KEY_SUNDO\n");break;
		case KEY_SUSPEND : mvwprintw(win,6,10,"key KEY_SUSPEND\n");break;
		case KEY_UNDO : mvwprintw(win,6,10,"key KEY_UNDO\n");break;
		case KEY_MOUSE : mvwprintw(win,6,10,"key KEY_MOUSE\n");break;
		case KEY_RESIZE : mvwprintw(win,6,10,"key KEY_RESIZE\n");break;
		case KEY_EVENT : mvwprintw(win,6,10,"key KEY_EVENT\n");break;
		case KEY_F(1) : mvwprintw(win,6,10,"key F1\n");break;
		default : mvwprintw(win,6,10,"unknown key %x\n",ch);break;
	}
	}

	return 0;
}



int		SCROLLWINDOW_print(SCROLLWINDOW *scw)
{
	int		y,x,i,l,k;
	char	buf[256];
	
	getmaxyx(scw->win,y,x);
	//scw->stop = y - BTMBORDER;
	memset(buf,' ',sizeof(buf));

	for(i=scw->start,k=TOPBORDER;(i < scw->stop) && (k < y-BTMBORDER); i++,k++)
	{
		l = snprintf(buf,x-2," %s",scw->names[i]);
		memset(buf+l,' ',sizeof(buf)-l);
		buf[y] = 0;
		mvwprintw(scw->win,k,1,buf);
	}
	wrefresh(scw->win);
	return 0;
}



char 	**createNames(int count)
{
	int		i;
	char	**names;
	char	buf[16];

	names = (char **)malloc(count * sizeof(char *));
	
	for(i=1;i<=count;i++)
	{
		sprintf(buf,"%08d",i);
		names[i-1] = strdup(buf);
	}
	return names;
}
