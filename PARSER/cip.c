#include <stdio.h>
#include <string.h>
#include "parser.h"


char	*CLIST[] = {
	"NULL",
	"SSL3-RC4-MD5",
	"SSL3-RC4-SHA",
	"SSL3-DES-CBC3-SHA",
	"SSL3-DES-CBC-SHA",
	"TLS1-EXP1024-RC4-SHA",
	"TLS1-AES-256-CBC-SHA",
	"TLS1-AES-128-CBC-SHA",
	"SSL3-EXP-RC4-MD5",
	"SSL3-EXP-DES-CBC-SHA",
	"SSL3-EXP-RC2-CBC-MD5",
	"SSL2-RC4-MD5",
	"SSL2-DES-CBC3-MD5",
	"SSL2-RC2-CBC-MD5",
	"SSL2-DES-CBC-MD5",
	"SSL2-RC4-64-MD5",
	"SSL2-EXP-RC4-MD5",
	"SSL3-EDH-DSS-DES-CBC3-SHA",
	"SSL3-EDH-DSS-DES-CBC-SHA",
	"TLS1-EXP1024-DHE-DSS-DES-CBC-SHA",
	"TLS1-DHE-DSS-RC4-SHA",
	"TLS1-EXP1024-DHE-DSS-RC4-SHA",
	"TLS1-DHE-DSS-AES-256-CBC-SHA",
	"SSL3-EXP-EDH-DSS-DES-CBC-SHA",
	"TLS1-DHE-DSS-AES-128-CBC-SHA",
	"SSL3-EDH-RSA-DES-CBC3-SHA",
	"SSL3-EDH-RSA-DES-CBC-SHA",
	"SSL3-EXP-EDH-RSA-DES-CBC-SHA",
	"TLS1-DHE-RSA-AES-256-CBC-SHA",
	"TLS1-DHE-RSA-AES-128-CBC-SHA",
	"TLS1-EXP1024-RC4-MD5",
	"TLS1-EXP1024-RC2-CBC-MD5",
	"SSL2-EXP-RC2-CBC-MD5",
	"SSL3-ADH-RC4-MD5",
	"SSL3-ADH-DES-CBC3-SHA",
	"SSL3-ADH-DES-CBC-SHA",
	"TLS1-ADH-AES-128-CBC-SHA",
	"TLS1-ADH-AES-256-CBC-SHA",
	"SSL3-EXP-ADH-RC4-MD5",
	"SSL3-EXP-ADH-DES-CBC-SHA",
	"SSL3-NULL-MD5",
	"SSL3-NULL-SHA",
	"TLS1-ECDHE-RSA-RC4-SHA",
	"TLS1-ECDHE-RSA-DES-CBC3-SHA",
	"TLS1-ECDHE-RSA-AES128-SHA",
	"TLS1-ECDHE-RSA-AES256-SHA",
	"TLS1.2-AES128-GCM-SHA256",
	"TLS1.2-AES256-GCM-SHA384",
	"TLS1.2-DHE-RSA-AES128-GCM-SHA256",
	"TLS1.2-DHE-RSA-AES256-GCM-SHA384",
	"TLS1.2-ECDHE-RSA-AES128-GCM-SHA256",
	"TLS1.2-ECDHE-RSA-AES256-GCM-SHA384",
	"TLS1.2-ECDHE-RSA-AES-128-SHA256",
	"TLS1.2-ECDHE-RSA-AES-256-SHA384",
	"TLS1.2-AES-256-SHA256",
	"TLS1.2-AES-128-SHA256",
	"TLS1.2-DHE-RSA-AES-128-SHA256",
	"TLS1.2-DHE-RSA-AES-256-SHA256",
	NULL
};

char *ALIST[] = {
"NULL", "ALL", "DEFAULT", "kRSA", "kEDH",
"DH", "EDH", "aRSA", "aDSS", "aNULL", "DSS",
"DES", "3DES", "RC4", "RC2", "eNULL", "MD5", 
"SHA1", "SHA", "NULL", "RSA", "ADH", "SSLv2",
"SSLv3", "TLSv1", "TLSv1_ONLY", "EXP", "EXPORT", 
"EXPORT40", "EXPORT56", "LOW", "MEDIUM", "HIGH",
"AES", "FIPS", "ECDHE", "AES-GCM", "SHA2", NULL
};


int	isAliasName(char *name)
{
	int	i=1;
	char	*ptr;

	while(ptr = ALIST[i++])
		if(strcmp(name,ptr)==0)
			return 1;

	return 0;
}


int	getNameToIndex(char *name)
{
	int	i=1;
	char	*ptr;

	while(ptr = CLIST[i])
		if(strcmp(name,ptr)==0)
			return i;
		else
			i++;

	return -1;
}


CTRIE_t *addNameToTrie(char *name,CTRIE_t *trie)
{
	int	i;
	CTRIE_t	*ct;

	if((i=getNameToIndex(name)) < 0)
		return NULL;

	if(trie->T[i])
		ct = trie->T[i];
	else
	{
		ct = (CTRIE_t *)Malloc(sizeof(CTRIE_t));
		ct->L = (LIST_t *)Malloc(sizeof(LIST_t));
		initList(ct->L,32);
		trie->T[i] = ct;
		ct->U = trie;
		ct->name =  CLIST[i];
	}
	return ct;
}


int	setTrieName(char *name,CTRIE_t *trie)
{
	strcpy(trie->name,name);
	return 0;
}



int	initList(LIST_t *l,int num)
{
	l->max = num;
	l->cur = 0;
	l->v   = (void **)Malloc(num * sizeof(void *));
	return 0;
}


int	addToList(LIST_t *l, void *v)
{
	void **tmp;
	int	sz = sizeof(void *);

	if(l->cur == l->max)
	{
		//ashoke_debug();
		tmp   = (void **)Malloc(l->max * 2 * sz);
		bcopy(l->v,tmp,l->max * sz); 
		l->max *= 2;
		free(l->v);
		l->v = tmp;	
	}
	l->v[l->cur++] = v;
	return 0;
}


int	freeList(LIST_t *l)
{
	free(l->v);
	free(l);
	return 0;
}

int	reInitList(LIST_t *L)
{
	int	i;
	
	for(i=0;i<L->cur;i++)
	{
		L->v[i] = NULL;
	}
	L->cur = 0;
	return 0;
}


LIST_t	*TrieToList(CTRIE_t *t)
{
	LIST_t	*L = (LIST_t *)Malloc(sizeof(LIST_t));
	int 	i,j;
	void	*v;

	initList(L,32);
	while(t && t->name)
	{
		addToList(L,t->name);
		t = t->U;
	}

	/* Reverse list */
	i = 0;
	j = L->cur - 1;
	while(i < j)
	{
		v = L->v[i];
		L->v[i] = L->v[j];
		L->v[j] = v;
		i++;
		j--;
	}
	
	return L;
}



int	sortList(LIST_t *L, cmpFn fn)
{
	int		i,j,minj;
	void	*minV=NULL;

	if(L->cur <= 1)
		return 0;

	for(i=0; i<L->cur; i++)
	{
		minV = L->v[i];
		minj = i;
		for(j=i; j<L->cur; j++)
		{
			if(fn(L->v[j],minV) < 0)
			{
				minV = L->v[j];
				minj = j;
			}
		}
		L->v[minj] = L->v[i];
		L->v[i] = minV;
	}

	return 0;
}



int	freeAttr(SET_ATTR_t *a)
{
	freeList(a->vList);
	freeList(a->sList);
	free(a->serviceList);
	free(a->vserverList);
	free(a);
	return 0;
}


int	ashoke_debug()
{
	//printf("ashoke_debug...\n");
	return 0;
}
