#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.h"

STMT_t		STMT;
SET_ATTR_t	SetAttr;
SSL_PARAMS_t SSLParams;
int 		rule_matched = 0;
int			PY=0;
int			PL=0;
int 		debugLine = 0;
int 		lineNo = 0;
int			curstate = 0;
int			batchmode = 0;


VSERVER_t	*vserver_list = NULL;
VSERVER_t	**vserver_list_tail = &vserver_list;

SERVICE_t	*service_list = NULL;
SERVICE_t	**service_list_tail = &service_list;

SET_ATTR_t	*attr_list = NULL;
SET_ATTR_t	**attr_list_tail = &attr_list;

SET_ATTR_t	*final_attr_list = NULL;
SET_ATTR_t	**final_attr_list_tail = &final_attr_list;

CIPHERGROUP_t	*ciphergroup_list = NULL;
CIPHERGROUP_t	**ciphergroup_list_tail = &ciphergroup_list;

CIPHERGROUP_t	*dynamic_ciphergroup_list = NULL;
CIPHERGROUP_t	**dynamic_ciphergroup_list_tail = &dynamic_ciphergroup_list;

CIPHERGROUP_t	*alias_ciphergroup_list = NULL;
CIPHERGROUP_t	**alias_ciphergroup_list_tail = &alias_ciphergroup_list;

CTRIE_t  *ctrie_head = NULL;
FILE	 *outfp = NULL;

VSERVER_t *handleAddVserver(char *type,char *name,int isVserver)
{
	VSERVER_t	*v = (VSERVER_t *)Malloc(sizeof(VSERVER_t));

	strcpy(v->name,name);
	strcpy(v->type,type);
	v->isVserver = isVserver;
	*vserver_list_tail = v;
	vserver_list_tail = &v->next;
	return v;
}


/* We shall treat service also as vserver entity with
 * isVserver not set.
 */
int	handleAddService(char *name)
{
	VSERVER_t	*v = (VSERVER_t *)Malloc(sizeof(VSERVER_t));
	strcpy(v->name,name);
	v->isVserver = 0;
	*vserver_list_tail = v;
	vserver_list_tail = &v->next;
	return 0;
}



int	handleSetVserver(char *name,SET_ATTR_t *attr,int isVserver)
{
	SET_ATTR_t	*a = findMatchingAttr(attr,isVserver);
	VSERVER_t	*v = findVserver(name,isVserver);

	if(!v)
		return -1;

	/* For internal services. the profile is a frontend one */
	if(v->isInternal)
		a = findMatchingAttr(attr,1);

	if(!a)
	{
		a = (SET_ATTR_t *)Malloc(sizeof(SET_ATTR_t));
		a->U = attr->U;
		a->core = attr->core;

		a->vList = (LIST_t *)Malloc(sizeof(LIST_t));
		initList(a->vList,32);
		a->sList = (LIST_t *)Malloc(sizeof(LIST_t));
		initList(a->sList,32);

		a->isVserver = isVserver;
		*attr_list_tail = a;
		attr_list_tail = &a->next;

		if(v->isInternal)
			a->isVserver = 1;
	}
	v->attr = a;
	if(a->isVserver)
		addToList(a->vList,v);
	else
		addToList(a->sList,v);
	return 0;
}


int	handleSSLParams(SSL_PARAMS_t *p)
{
	if(p->P.param_bits._denySSLReneg)
	{
		printf("denySSLReneg %s\n",p->param_core.denySSLReneg);
	}
	if(p->P.param_bits._dropReqWithNoHostHeader)
	{
		printf("dropReqWithNoHostHeader %s\n",p->param_core.dropReqWithNoHostHeader ? "YES":"NO");
	}
	if(p->P.param_bits._encryptTriggerPktCount)
	{
		printf("encryptTriggerPktCount %d\n",p->param_core.encryptTriggerPktCount);
	}
	if(p->P.param_bits._insertionEncoding)
	{
		printf("insertionEncoding %s\n",p->param_core.insertionEncoding);
	}
	if(p->P.param_bits._pushEncTriggerTimeout)
	{
		printf("pushEncTriggerTimeout %d\n",p->param_core.pushEncTriggerTimeout);
	}
	if(p->P.param_bits._pushFlag)
	{
		printf("pushFlag %s\n",p->param_core.pushFlag);
	}
	if(p->P.param_bits._quantumSize)
	{
		printf("quantumSize %d\n",p->param_core.quantumSize);
	}
	if(p->P.param_bits._sendCloseNotify)
	{
		printf("sendCloseNotify %s\n",p->param_core.sendCloseNotify ? "YES":"NO");
	}
	if(p->P.param_bits._sslTriggerTimeout)
	{
		printf("sslTriggerTimeout %d\n",p->param_core.sslTriggerTimeout);
	}
	if(p->P.param_bits._strictCAChecks)
	{
		printf("strictCAChecks %s\n",p->param_core.strictCAChecks ? "YES":"NO");
	}
	return 0;
}



SET_ATTR_t	*NewAttr(SET_ATTR_t *attr)
{
	SET_ATTR_t	*a = NULL;
	
	a = (SET_ATTR_t *)Malloc(sizeof(SET_ATTR_t));
	if(!a)
		return a;

	a->vList = (LIST_t *)Malloc(sizeof(LIST_t));
	initList(a->vList,32);
	a->sList = (LIST_t *)Malloc(sizeof(LIST_t));
	initList(a->sList,32);

	*attr_list_tail = a;
	attr_list_tail = &a->next;

	if(attr)
	{
		a->U = attr->U;
		a->core = attr->core;
	}
	else
		a->U.flag = 0;

	return a;
}



#if 0
int	handleSetService(char *name,SET_ATTR_t *attr)
{
	SET_ATTR_t	*a = findMatchingAttr(attr);
	VSERVER_t	*v = findVserver(name,0);

	if(!v)
		return -1;

	if(!a)
	{
		a = (SET_ATTR_t *)Malloc(sizeof(SET_ATTR_t));
		a->U = attr->U;
		a->core = attr->core;

		a->vList = (LIST_t *)Malloc(sizeof(LIST_t));
		initList(a->vList,32);
		a->sList = (LIST_t *)Malloc(sizeof(LIST_t));
		initList(a->sList,32);

		*attr_list_tail = a;
		attr_list_tail = &a->next;
	}

	v->attr = a;
	//addAttrService(a,s);
	addToList(a->sList,v);
	return 0;
}
#endif


int	handleBindVserverECCCurve(char *vname,char *curve,int isVserver)
{
	VSERVER_t		*v = findVserver(vname,isVserver);
	SET_ATTR_t		a,*ap;

	if(!v)
		return -1;

	if(!v->attr)
	{
		a.U.flag = 0;
		ap = findMatchingAttr(&a,isVserver);
		if(ap)
			v->attr = ap;
		else
		{
			v->attr = NewAttr(NULL);
			v->attr->isVserver = isVserver;
		}

		if(isVserver)	
			addToList(v->attr->vList,v);
		else
			addToList(v->attr->sList,v);
	}

	if(strcmp(curve,CURVE_256)==0)
		v->ecc_curve |= ECCCURVE_P_256;
	else if(strcmp(curve,CURVE_384)==0)
		v->ecc_curve |= ECCCURVE_P_384;
	else if(strcmp(curve,CURVE_224)==0)
		v->ecc_curve |= ECCCURVE_P_224;
	else if(strcmp(curve,CURVE_521)==0)
		v->ecc_curve |= ECCCURVE_P_521;
	
	return 0;
}



int	handleBindVserverCipher(char *vname,char *cname,int isVserver)
{
	CIPHERGROUP_t	*c = findCipherGroup(cname);
	VSERVER_t		*v = findVserver(vname,isVserver);
	CTRIE_t			*trie;
	SET_ATTR_t		a,*ap;

	if(!v)
		return -1;
	if(!v->attr)
	{
		a.U.flag = 0;
		ap = findMatchingAttr(&a,isVserver);
		if(ap)
			v->attr = ap;
		else
		{
			v->attr = NewAttr(NULL);
			v->attr->isVserver = isVserver;
		}

		if(isVserver)
			addToList(v->attr->vList,v);
		else
			addToList(v->attr->sList,v);
	}

	if(c)
	{
		v->cgp = c;
	}
	else
	{
		trie = (v->cur_trie ? v->cur_trie : ctrie_head);
		v->cur_trie = addNameToTrie(cname,trie);
	}

	return 0;
}



#if 0
int	handleBindServiceCipher(char *sname,char *cname)
{
	CIPHERGROUP_t	*c = findCipherGroup(cname);
	//SERVICE_t		*s = findService(sname);
	VSERVER_t		*v = findVserver(vname,0);
	CTRIE_t			*trie;

	if(!s)
		return -1;

	if(c)
	{
		s->cgp = c;
	}
	else
	{
		trie = (s->cur_trie ? s->cur_trie : ctrie_head);
		s->cur_trie = addNameToTrie(cname,trie);
	}

	return 0;
}
#endif



int	handleAddCipherGroup(char *gname)
{
	CIPHERGROUP_t	*v = (CIPHERGROUP_t *)Malloc(sizeof(CIPHERGROUP_t));
	bzero(v,sizeof(CIPHERGROUP_t));
	strcpy(v->name,gname);
	*ciphergroup_list_tail = v;
	ciphergroup_list_tail = &v->next;
	return 0;
}




int	handleBindCipherGroup(char *gname,char *cname)
{
	CIPHERGROUP_t	*head = findCipherGroup(gname);

	if(!head)
		return -1;
	strcpy(head->cipher[head->idx++],cname);	
	return 0;
}




CIPHERGROUP_t	*findCipherGroup(char *name)
{
	CIPHERGROUP_t	*head = ciphergroup_list;
	while(head)
	{
		if(strcmp(head->name,name)==0)
			break;
		head = head->next;
	}
	if(!head)
	{
		if(isAliasName(name))
			head = AddAliasCipherGroup(name); 
	}
	return head;
}




VSERVER_t	*findVserver(char *name,int isVserver)
{
	VSERVER_t	*head = vserver_list;
	while(head)
	{
		if((strcmp(head->name,name)==0) && head->isVserver == isVserver)
			break;
		head = head->next;
	}
	if(!head && (isVserver==0))
	{
		/* we are here for internal services. but for internal services we need
		 * front end profile. so treat it as vserver
		 */
		head = handleAddVserver("service",name,isVserver);
		head->isInternal = 1;
	}
	return head;
}



#if 0
VSERVER_t	*findService(char *name)
{
	//SERVICE_t	*head = service_list;
	VSERVER_t	*head = vserver_list;
	while(head)
	{
		if((strcmp(head->name,name)==0) && !head->isVserver)
			break;
		head = head->next;
	}
	return head;
}
#endif



int	addAttr(SET_ATTR_t *a)
{
	*attr_list_tail = a;
	attr_list_tail = &a->next;
}




SET_ATTR_t	*findMatchingAttr(SET_ATTR_t *a,int isVserver)
{
	SET_ATTR_t	*head = attr_list;
	while(head)
	{
		if(isVserver == head->isVserver)
		{
			if(cmpAttribs(head,a) == 0)
				break;
		}
		head = head->next;
	}
	return head;
}




int	cmpAttribs(SET_ATTR_t *a, SET_ATTR_t *b)
{
	int	ret = 1;

	do
	{
		if(a->U.flag != b->U.flag)
			break;

		if(a->U.bits._dh && (a->core._dhCount != b->core._dhCount))
			break;
		if(a->U.bits._eRSA && (a->core._eRSACount != b->core._eRSACount))
			break;
		if(a->U.bits._sessTimeout && (a->core._sessTimeout != b->core._sessTimeout))
			break;
		if(a->U.bits._clearTextPort && (a->core._clearTextPort != b->core._clearTextPort))
			break;

		if(a->U.bits._dh && (strcmp(a->core._dhFile,b->core._dhFile)) )
			break;
		if(a->U.bits._cipherRedirect && (strcmp(a->core._cipherURL,b->core._cipherURL)) )
			break;
		if(a->U.bits._sslv2Redirect && (strcmp(a->core._sslv2URL,b->core._sslv2URL)) )
			break;
		if(a->U.bits._serverAuth && (strcmp(a->core._commonName,b->core._commonName)))
			break;
		if(a->U.bits._dtlsProfileName && (strcmp(a->core._dtlsProfileName,b->core._dtlsProfileName)))
			break;
		if(a->U.bits._sslProfile && (strcmp(a->core._sslProfile,b->core._sslProfile)))
			break;
		if(a->U.bits._pushEncTrigger && (strcmp(a->core._pushEncTrigger,b->core._pushEncTrigger)))
			break;
		if(a->U.bits._clientAuth && (strcmp(a->core._clientCert,b->core._clientCert)) )
			break;
	
		ret = 0;
	} while (0);

	return ret;
}




int	addAttrVserver(SET_ATTR_t *attr, VSERVER_t *v)
{
	if(attr->curVserverIdx == attr->maxVserverCount)
	{
		int	max = attr->maxVserverCount * 2;
		VSERVER_t	**vl = (VSERVER_t **)Malloc(max * sizeof(VSERVER_t *));

		bcopy(attr->vserverList,vl, attr->maxVserverCount * sizeof(VSERVER_t *));
		attr->maxVserverCount = max;
		free(attr->vserverList);
		attr->vserverList = vl;
	}
	attr->vserverList[attr->curVserverIdx++] = v;
	return 0;
}




int	addAttrService(SET_ATTR_t *attr, SERVICE_t *s)
{
	if(attr->curServiceIdx == attr->maxServiceCount)
	{
		int	max = attr->maxServiceCount * 2;
		SERVICE_t	**sl = (SERVICE_t **)Malloc(max * sizeof(SERVICE_t *));;

		bcopy(attr->serviceList,sl, attr->maxServiceCount * sizeof(SERVICE_t *));
		attr->maxServiceCount = max;
		free(attr->serviceList);
		attr->serviceList = sl;
	}
	attr->serviceList[attr->curServiceIdx++] = s;
	return 0;
}




CIPHERGROUP_t *listToDynamicCipherGroup(char *grpName,LIST_t *L)
{
	CIPHERGROUP_t	*cg = (CIPHERGROUP_t *)Malloc(sizeof(CIPHERGROUP_t));

	strcpy(cg->name,grpName);
	for(cg->idx=0;cg->idx<L->cur;cg->idx++)
		strcpy(cg->cipher[cg->idx],(char *)(L->v[cg->idx]));

	*dynamic_ciphergroup_list_tail = cg;
	dynamic_ciphergroup_list_tail  = &(cg->next);
	return cg;
}




int PrintToDynamicCipherGroup()
{
	int		i;
	CIPHERGROUP_t	*head = dynamic_ciphergroup_list;

	while(head)
	{
		printf("add ssl cipher %s\n",head->name);
		for(i=0;i<head->idx;i++)
			printf("bind ssl cipher %s -cipherName %s\n",head->name,head->cipher[i]);
		printf("\n");
	}
	return 0;
}






CIPHERGROUP_t	*AddAliasCipherGroup(char *grpName)
{
	CIPHERGROUP_t *cgp = alias_ciphergroup_list;
	while(cgp)
	{
		if(strcmp(cgp->name,grpName)==0)
			return cgp;
		cgp = cgp->next;
	}
	cgp = (CIPHERGROUP_t *)Malloc(sizeof(CIPHERGROUP_t));
	strcpy(cgp->name,grpName);
	*alias_ciphergroup_list_tail = cgp;
	alias_ciphergroup_list_tail = &cgp->next;
	return cgp;
}




int	AddDynamicCipherGroup()
{
	LIST_t		trieL;
	LIST_t		L;
	LIST_t		*Lp;
	VSERVER_t	*head = vserver_list,*V;
	CIPHERGROUP_t	*cgp;
	CTRIE_t		*T;

	int		i,j;
	char	grpName[128];

	initList(&trieL,64);
	while(head)
	{
		if(head->cur_trie )
		{
			if(!head->cur_trie->pushed)
			{
				addToList(&trieL,head->cur_trie);
				head->cur_trie->pushed = 1;
			}
			addToList(head->cur_trie->L,head);
		}
		head = head->next;
	}

	initList(&L,32);
	for(i=0;i<trieL.cur;i++)
	{
		T = (CTRIE_t *)(trieL.v[i]);
		Lp = TrieToList(T);

#if 0
		printf("\n\n");
		printf("Please enter Cipher Group Name for the following ciphers :\n");
		printf("----------------------------------------------------------\n");
		for(j=0;j<Lp->cur;j++)
			printf("	%s\n",Lp->v[j]);
		printf("Cipher Group Name :");
		scanf("%s",grpName);
#endif
		
		strcpy(grpName,"TO FILLE");

		cgp = listToDynamicCipherGroup(grpName,Lp);
		freeList(Lp);

		for(j=0;j<T->L->cur;j++)
		{
			V = (VSERVER_t *)(T->L->v[j]);
			V->cgp = cgp;	
		}
	}
	return 0;
}




int	NameDynamicCipherGroup()
{
	CIPHERGROUP_t	*head = dynamic_ciphergroup_list;
	int	i;
	
	while(head)
	{
		if(batchmode)
			getNextCipherGroupName(head->name);
		else
		{
			printf("\n\n");
			printf("Please enter Cipher Group Name for the following ciphers :\n");
			printf("----------------------------------------------------------\n");
		
			for(i=0;i<head->idx;i++)
				printf("	%s\n",head->cipher[i]);
			printf("\n");

			printf("Cipher Group Name: ");
			scanf("%s",head->name);
		}

		head = head->next;
	}

	return 0;
}



#if 0
int	postParse()
{
	int				i,j;
	int				ecc_curve;
	SET_ATTR_t		*attrHead = attr_list, *tmpAttr;
	cmpFn			fn = vserverCipherGrpCmp;
	CIPHERGROUP_t	*cgp;
	VSERVER_t		*vs;

	AddDynamicCipherGroup();

	while(attrHead)
	{
		sortList(attrHead->vList,fn);
		sortList(attrHead->sList,fn);


		i = attrHead->vList->cur - 1;
		cgp = ((VSERVER_t *)(attrHead->vList->v[i]))->cgp;
		ecc_curve = ((VSERVER_t *)(attrHead->vList->v[i]))->ecc_curve;

		tmpAttr = cloneAttr(attrHead);
		tmpAttr->cgp = cgp;
		tmpAttr->core._ecc_curve = ecc_curve;
		((VSERVER_t *)(attrHead->vList->v[i]))->attr = tmpAttr;

		addToList(tmpAttr->vList,attrHead->vList->v[i]);

		*final_attr_list_tail = tmpAttr;
		final_attr_list_tail = &tmpAttr->next;
	
		i--;

		while(i >= 0)
		{
			vs = (VSERVER_t *)(attrHead->vList->v[i]);
			if((vs->cgp == cgp) && (vs->ecc_curve == ecc_curve))
			{
				((VSERVER_t *)(attrHead->vList->v[i]))->attr = tmpAttr;
				addToList(tmpAttr->vList,attrHead->vList->v[i]);
			}
			else 
			{
				cgp = ((VSERVER_t *)(attrHead->vList->v[i]))->cgp;
				ecc_curve = ((VSERVER_t *)(attrHead->vList->v[i]))->ecc_curve;
				tmpAttr = cloneAttr(attrHead);
				tmpAttr->cgp = cgp;
				tmpAttr->core._ecc_curve = ecc_curve;
				((VSERVER_t *)(attrHead->vList->v[i]))->attr = tmpAttr;
				addToList(tmpAttr->vList,attrHead->vList->v[i]);
				*final_attr_list_tail = tmpAttr;
				final_attr_list_tail = &tmpAttr->next;
			}
			i--;
		}
		
		attr_list = attrHead->next;
		freeAttr(attrHead);
		attrHead = attr_list;
	}
	return 0;
}
#endif



int	PostParse()
{
	int				ecc_bypass = 0;
	int				i,j,k;
	int				ecc_curve;
	SET_ATTR_t		*attrHead = attr_list, *tmpAttr, **app;
	SET_ATTR_t		*fe_withssl3, *be_withssl3;
	cmpFn			fn = vserverCipherGrpCmp;
	CIPHERGROUP_t	*cgp;
	VSERVER_t		*vs, *vhead;

	LIST_t			*list[3], *listp;


	/* For the cases where no change was done to the vserver
	 * we would still would need a profile to turn of ssl3.
	 */ 
	fe_withssl3 = NewAttr(NULL);
	be_withssl3 = NewAttr(NULL);
	strcpy(fe_withssl3->core.name,"profile_withssl3");
	strcpy(be_withssl3->core.name,"profile_withssl3_backend");
	fe_withssl3->isVserver = 1;
	be_withssl3->isVserver = 0;

	vhead = vserver_list;
	while(vhead)
	{
		if(vhead->attr)
		{
			vhead = vhead->next;
			continue;
		}
		if(vhead->isVserver)
		{
			vhead->attr = fe_withssl3;
			addToList(fe_withssl3->vList,vhead);
		}
		else
		{
			vhead->attr = be_withssl3;
			addToList(be_withssl3->sList,vhead);
		}
		vhead = vhead->next;
	}


	AddDynamicCipherGroup();

	while(attrHead)
	{
		if(ISATTRSET(attrHead,ssl3))
		{
			DISABLEATTRONOFF(attrHead,ssl3);  //Disable if set
		}
		else
		{
			ENABLEATTRONOFF(attrHead,ssl3,1); //Enable if not set
		}

		
		sortList(attrHead->vList,fn);
		sortList(attrHead->sList,fn);

		list[0] = attrHead->vList;
		list[1] = attrHead->sList;
		list[2] = NULL;


		for(k=0;(listp = list[k]) ;k++)
		{
		if(!listp->cur)
			continue;
		i = listp->cur - 1;
		cgp = ((VSERVER_t *)(listp->v[i]))->cgp;
		ecc_curve = ((VSERVER_t *)(listp->v[i]))->ecc_curve;

		tmpAttr = cloneAttr(attrHead);
		tmpAttr->cgp = cgp;
		tmpAttr->core._ecc_curve = ecc_curve;
		((VSERVER_t *)(listp->v[i]))->attr = tmpAttr;

		if(attrHead->vList->cur)
			addToList(tmpAttr->vList,listp->v[i]);
		else
			addToList(tmpAttr->sList,listp->v[i]);

		*final_attr_list_tail = tmpAttr;
		final_attr_list_tail = &tmpAttr->next;
	
		i--;

		while(i >= 0)
		{
			vs = (VSERVER_t *)(listp->v[i]);
			if((vs->cgp == cgp) && (vs->ecc_curve == ecc_curve))
			{
				((VSERVER_t *)(listp->v[i]))->attr = tmpAttr;
				if(attrHead->vList->cur)
					addToList(tmpAttr->vList,listp->v[i]);
				else
					addToList(tmpAttr->sList,listp->v[i]);
			}
			else 
			{
				cgp = ((VSERVER_t *)(listp->v[i]))->cgp;
				ecc_curve = ((VSERVER_t *)(listp->v[i]))->ecc_curve;
				tmpAttr = cloneAttr(attrHead);
				tmpAttr->cgp = cgp;
				tmpAttr->core._ecc_curve = ecc_curve;
				((VSERVER_t *)(listp->v[i]))->attr = tmpAttr;

				if(attrHead->vList->cur)
					addToList(tmpAttr->vList,listp->v[i]);
				else
					addToList(tmpAttr->sList,listp->v[i]);

				*final_attr_list_tail = tmpAttr;
				final_attr_list_tail = &tmpAttr->next;
			}
			i--;
		}
		}

		attr_list = attrHead->next;
		freeAttr(attrHead);
		attrHead = attr_list;
	}

	/* This Profile has only default values, that is not attrib change 
	 * ecc curves not modified and no cipher changes .. 
	 */

	for(app = &final_attr_list; tmpAttr = *app;)
	{
		ecc_bypass = 0;
		if((*app)->isVserver)
		{
			if(tmpAttr->core._ecc_curve == 15)
				ecc_bypass = 1;
		}
		else
		{
			if(tmpAttr->core._ecc_curve == 0)
				ecc_bypass = 1;
		}

		if((tmpAttr->U.flag == 0) && ecc_bypass && !tmpAttr->cgp)
		{
			*app = tmpAttr->next;
			tmpAttr->next = NULL;
			freeAttr(tmpAttr);
			continue;
		}
		app = &tmpAttr->next;
	}

#if 0
	attrHead = final_attr_list; 
	while(attrHead)
	{
		if((attrHead->U.flag == 0) && (attrHead->core._ecc_curve == 15) && !attrHead->cgp)
		{
			final_attr_list = attrHead->next;
			freeAttr(attrHead);
			attrHead = final_attr_list;
			continue;
		}
		attrHead = attrHead->next;
	}
#endif

	return 0;
}



int		vserverCipherGrpCmp(void *v1, void *v2)
{
	VSERVER_t	*V1 = (VSERVER_t *)v1;
	VSERVER_t	*V2 = (VSERVER_t *)v2;

	if(V1->cgp > V2->cgp)
		return 1;
	else if(V1->cgp == V2->cgp)
		return 0;
	if(V1->cgp < V2->cgp)
		return -1;
}




SET_ATTR_t *cloneAttr(SET_ATTR_t *attr)
{
	SET_ATTR_t	*a = (SET_ATTR_t *)Malloc(sizeof(SET_ATTR_t));
	a->U = attr->U;
	a->core = attr->core;
	a->isVserver = attr->isVserver;
	a->vList = (LIST_t *)Malloc(sizeof(LIST_t));
	a->sList = (LIST_t *)Malloc(sizeof(LIST_t));
	initList(a->vList,32);
	initList(a->sList,32);
	return a;
}



int	nameProfile()
{
	SET_ATTR_t	*head = final_attr_list;
	VSERVER_t	*v;
	LIST_t		*listp;
	int			i;
	int			isVserver = 0;

	while(head)
	{
		isVserver = 0;

		if(head->vList->cur > 0)
		{
			isVserver = 1;
			listp = head->vList;
		}
		else
			listp = head->sList;

		if(batchmode)
			getNextProfileName(head->core.name);
		else
		{
			printf("\n\n");
			printf("Please enter Profile Name for the following %s :\n", isVserver ? "Vservers" : "Serives");
			printf("----------------------------------------------------------\n");

			for(i=0;i<listp->cur;i++)
			{
				v = (VSERVER_t *)(listp->v[i]);
				printf("	%s\n",v->name);
			}
			printf("Profile Name : ");
			scanf("%s",head->core.name);
			printf("\n");
		}

		head = head->next;
	}
	return 0;
}





int	PrintConfig()
{
	CIPHERGROUP_t	*cgp  = dynamic_ciphergroup_list;	
	SET_ATTR_t		*attr = final_attr_list;
	SET_ATTR_t		*fe_withssl3, *be_withssl3;
	VSERVER_t		*vhead = vserver_list;
	char			*YESNO;

	while(cgp)
	{
		PrintACipherGroup(cgp);
		cgp = cgp->next;
	}

	while(attr)
	{
		if(attr->vList->cur == 0)
		{
			attr = attr->next;
			continue;
		}
		printf("##########################################################\n");
		printf("#  Profile Start (%s):  \n",attr->core.name);
		printf("##########################################################\n\n");

		PrintAProfile(attr);
		printf("\n");
		PrintOneBoundProfile(attr);
		printf("\n\n\n");
		attr = attr->next;
	}
	printf("\n");

	attr = final_attr_list;
	while(attr)
	{
		if(attr->vList->cur != 0)
		{
			attr = attr->next;
			continue;
		}
		printf("##########################################################\n");
		printf("#  Profile Start (%s):  \n",attr->core.name);
		printf("##########################################################\n\n");

		PrintAProfile(attr);
		printf("\n");
		PrintOneBoundProfile(attr);
		printf("\n\n\n");
		attr = attr->next;
	}
	printf("\n");


	if(SSLParams.P.flag)
	{
		printf("\n");
		printf("set ssl profile ns_default_ssl_profile_frontend  ");
	}

	if(SSLParams.P.param_bits._denySSLReneg)
	{
		printf("-denySSLReneg %s  ", SSLParams.param_core.denySSLReneg);
	}

	if(SSLParams.P.param_bits._dropReqWithNoHostHeader)
	{
		YESNO = SSLParams.param_core.dropReqWithNoHostHeader ? "YES":"NO";
		printf("-dropReqWithNoHostHeader %s  ",YESNO);
	}

	if(SSLParams.P.param_bits._encryptTriggerPktCount)
	{
		printf("-encryptTriggerPktCount %d  ",SSLParams.param_core.encryptTriggerPktCount);
	}

	if(SSLParams.P.param_bits._insertionEncoding)
	{
		printf("-insertionEncoding %s  ",SSLParams.param_core.insertionEncoding);
	}

	if(SSLParams.P.param_bits._pushEncTriggerTimeout)
	{
		printf("-pushEncTriggerTimeout %d  ",SSLParams.param_core.pushEncTriggerTimeout);
	}

	if(SSLParams.P.param_bits._pushFlag)
	{
		printf("-pushFlag %d  ",SSLParams.param_core.pushFlag);
	}

	if(SSLParams.P.param_bits._quantumSize)
	{
		printf("-quantumSize %d  ",SSLParams.param_core.quantumSize);
	}

	if(SSLParams.P.param_bits._sendCloseNotify)
	{
		YESNO = SSLParams.param_core.sendCloseNotify ? "YES":"NO";
		printf("-sendCloseNotify %s  ",YESNO);
	}

	if(SSLParams.P.param_bits._sslTriggerTimeout)
	{
		printf("-sslTriggerTimeout %d  ",SSLParams.param_core.sslTriggerTimeout);
	}

	if(SSLParams.P.param_bits._strictCAChecks)
	{
		YESNO = SSLParams.param_core.strictCAChecks ? "YES":"NO";
		printf("-strictCAChecks %s",YESNO);
	}
	printf("\n\n");

	return 0;
}


int	PrintACipherGroup(CIPHERGROUP_t *cgp)
{
	int		i;

	printf("add ssl cipher %s\n",cgp->name);
	for(i=0;i<cgp->idx;i++)
		printf("bind ssl cipher %s -cipherName %s\n",cgp->name,cgp->cipher[i]);
	printf("\n");

	return 0;
}



int	PrintAProfile(SET_ATTR_t *attr)
{
	char	*buf = malloc(2048);
	char	*YESNO;

	bzero(buf,2048);
	writeProfile(attr,buf);

	printf("add ssl profile %s ",attr->core.name);
	if(attr->sList->cur > 0)
		printf("-sslProfileType BackEnd");
	printf("\n\n");

	if(strlen(buf))
		printf("set ssl profile %s %s\n",attr->core.name,buf);


	/* When we create a Profile, it is by default attached to 
	 * ALL  ecc curves. So, we dont have to do anything for ALL
	 * case. For other cases, we first unbind all ciphers and then
	 * add specific ones.
	 */
	if(attr->core._ecc_curve != 15)
	{
		if(attr->isVserver)
			printf("unbind ssl profile %s -eccCurveName ALL\n",attr->core.name);

		if(attr->core._ecc_curve & ECCCURVE_P_256)
		printf("bind ssl profile %s -eccCurveName %s\n",attr->core.name,CURVE_256);
		if(attr->core._ecc_curve & ECCCURVE_P_384)
		printf("bind ssl profile %s -eccCurveName %s\n",attr->core.name,CURVE_384);
		if(attr->core._ecc_curve & ECCCURVE_P_224)
		printf("bind ssl profile %s -eccCurveName %s\n",attr->core.name,CURVE_224);
		if(attr->core._ecc_curve & ECCCURVE_P_521)
		printf("bind ssl profile %s -eccCurveName %s\n",attr->core.name,CURVE_521);
	}


	if(SSLParams.P.flag)
	{
		printf("\n");
		printf("set ssl profile %s  ",attr->core.name);
	}

	if(SSLParams.P.param_bits._denySSLReneg)
	{
		printf("-denySSLReneg %s  ",SSLParams.param_core.denySSLReneg);
	}

	if(SSLParams.P.param_bits._dropReqWithNoHostHeader)
	{
		YESNO = SSLParams.param_core.dropReqWithNoHostHeader ? "YES":"NO";
		printf("-dropReqWithNoHostHeader %s  ",YESNO);
	}

	if(SSLParams.P.param_bits._encryptTriggerPktCount)
	{
		printf("-encryptTriggerPktCount %d  ",SSLParams.param_core.encryptTriggerPktCount);
	}

	if(SSLParams.P.param_bits._insertionEncoding)
	{
		printf("-insertionEncoding %s  ",SSLParams.param_core.insertionEncoding);
	}

	if(SSLParams.P.param_bits._pushEncTriggerTimeout)
	{
		printf("-pushEncTriggerTimeout %d  ",SSLParams.param_core.pushEncTriggerTimeout);
	}

	if(SSLParams.P.param_bits._pushFlag)
	{
		printf("-pushFlag %d  ",SSLParams.param_core.pushFlag);
	}

	if(SSLParams.P.param_bits._quantumSize)
	{
		printf("-quantumSize %d  ",SSLParams.param_core.quantumSize);
	}

	if(SSLParams.P.param_bits._sendCloseNotify)
	{
		YESNO = SSLParams.param_core.sendCloseNotify ? "YES":"NO";
		printf("-sendCloseNotify %s  ",YESNO);
	}

	if(SSLParams.P.param_bits._sslTriggerTimeout)
	{
		printf("-sslTriggerTimeout %d  ",SSLParams.param_core.sslTriggerTimeout);
	}

	if(SSLParams.P.param_bits._strictCAChecks)
	{
		YESNO = SSLParams.param_core.strictCAChecks ? "YES":"NO";
		printf("-strictCAChecks %s",YESNO);
	}
	printf("\n\n");



	if(attr->cgp)
	{
		printf("unbind ssl profile %s -cipherName %s\n",attr->core.name,attr->isVserver ? "DEFAULT" : "ALL");
		printf("bind ssl profile %s -cipherName %s\n",attr->core.name,attr->cgp->name);
	}

	attr = attr->next;
	free(buf);

	return 0;
}



int	PrintOneBoundProfile(SET_ATTR_t *attr)
{
	int			i;
	char		*name;
	LIST_t		*listp = NULL;
	VSERVER_t	*v;

	if(attr->vList->cur)
		listp = attr->vList;
	else if(attr->sList->cur)
		listp = attr->sList;

	for(i=0;i<listp->cur;i++)
	{
		v = (VSERVER_t *)(listp->v[i]);
		//name = (v->isVserver ? "vserver": "service");
		name = (v->isVserver ? "vserver": v->type);
		printf("set ssl %s %s -sslprofile %s\n",name,v->name,attr->core.name);
	}
	return 0;
}



int	PrintBoundProfiles()
{
	int			i;
	SET_ATTR_t	*attr = final_attr_list;
	VSERVER_t	*v;
	LIST_t		*listp = NULL;
	char		*name;

	while(attr)
	{
		if(attr->vList->cur)
			listp = attr->vList;
		else if(attr->sList->cur)
			listp = attr->sList;

		for(i=0;i<listp->cur;i++)
		{
			v = (VSERVER_t *)(listp->v[i]);
			name = (v->isVserver ? "vserver": "service");
			printf("set ssl %s %s -sslprofile %s\n",name,v->name,attr->core.name);
		}
		attr = attr->next;
		printf("\n");
	}
	printf("\n\n");
	return 0;
}






int	writeProfile(SET_ATTR_t *a,char * buf)
{
#define	B	a->U.bits
#define	C	a->core

#define	 ONOFF(x) if(B._##x) \
		{l = sprintf(ptr," -%s %s", #x, (C._##x ? "ENABLED":"DISABLED")); ptr += l;}

#define	 YESNO(x) if(B._##x) \
		{l = sprintf(ptr," -%s %s", #x, (C._##x ? "YES":"NO")); ptr += l;}

#define	 INTX(x) if(B._##x) \
		{l = sprintf(ptr," -%s %d", #x, a->core._##x); ptr += l;}

#define	 STRX(x) if(B._##x) \
		{l = sprintf(ptr," -%s %s", #x, a->core._##x); ptr += l;}

	char	*ptr = buf;
	int		l = 0;


	ONOFF(dh);
	ONOFF(eRSA);
	ONOFF(clientAuth);
	ONOFF(sessReuse);
	ONOFF(cipherRedirect);
	ONOFF(sslv2Redirect);
	ONOFF(sslRedirect);
	ONOFF(redirectPortRewrite);
	ONOFF(nonFipsCiphers);
	ONOFF(SNIEnable);
	ONOFF(serverAuth);

	ONOFF(ssl2);
	ONOFF(ssl3);
	ONOFF(tls1);
	ONOFF(tls11);
	ONOFF(tls12);

	YESNO(sendCloseNotify);


	INTX(dhCount);
	INTX(eRSACount);
	INTX(sessTimeout);
	INTX(clearTextPort);

	STRX(dhFile);
	STRX(cipherURL);
	STRX(sslv2URL);
	STRX(commonName);
	STRX(dtlsProfileName);
	STRX(pushEncTrigger);
	STRX(clientCert);

	
	return 0;
}





int	debugY()
{
	int	ret = 0;
	if(PY)
		ret = 1;
	return ret;
}


int debugL()
{
	int	ret = 0;
	int line = debugLine - 1; //lineNo increments only at the end of line
	if(PL)
		if (!debugLine || (line && (line == lineNo)) )	ret = 1;

	return ret;
}



void * Malloc(int size)
{
	void *v = (void *)malloc(size);
	if(!v)
	{
		printf("Malloc failed. Exiting..\n");
		exit(0);
	}
	bzero(v,size);
	return v;
}



int	getNextProfileName(char *name)
{
	static int	id = 1;
	sprintf(name,"profile-%03d",id++);
	return 0;
}


int	getNextCipherGroupName(char *name)
{
	static int	id = 1;
	sprintf(name,"ciphergroup-%03d",id++);
	return 0;
}


int		DumpAttr(SET_ATTR_t *a)
{
	int			i,j,k;
	LIST_t		*l = NULL;
	VSERVER_t	*vs;

	printf("attr %p   isVserver %d flag %d\n",a,a->isVserver,a->U.flag);
	if(a->vList->cur)
		l = a->vList;
	else if(a->sList->cur)
		l = a->sList;
	for(i=0;l && (i<l->cur);i++)
	{
		vs = (VSERVER_t *)(l->v[i]);
		printf("	%s ",vs->name);
		printf("cgp %p ",((VSERVER_t *)(vs))->cgp);
		printf("ecc %d\n",((VSERVER_t *)(vs))->ecc_curve);
	}
	printf("\n");
	return 0;
}


int	DumpAttrList(SET_ATTR_t *alist)
{
	while(alist)
	{
		DumpAttr(alist);
		alist = alist->next;
	}
	return 0;
}
