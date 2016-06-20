#include <sys/types.h>


#define	ATTRONOFF(x) SetAttr.U.bits._##x = 1;\
	SetAttr.core._##x = (yylval.yy_onoff ? 1:0);

#define	ENABLEATTRONOFF(a,x,v) if(!a->U.bits._##x) {\
	a->U.bits._##x = 1;\
	a->core._##x = v;\
	}

#define	DISABLEATTRONOFF(a,x) if(a->U.bits._##x) {\
	a->U.bits._##x = 0;\
	a->core._##x = 0;\
	}

#define	ISATTRSET(a,x) (a->U.bits._##x)
#define	SETATTR(a,x) a->U.bits._##x=1;a->core._##x=1;


#define	ECCCURVE_P_256	1
#define	ECCCURVE_P_384	2
#define	ECCCURVE_P_224	4
#define	ECCCURVE_P_521	8


#define	CURVE_256		"P_256"
#define	CURVE_384		"P_384"
#define	CURVE_224		"P_224"
#define	CURVE_521		"P_521"

typedef struct _list_ {
	int	max;
	int	cur;
	void	**v;	
} LIST_t;


typedef struct _ctrie_ {
	char	*name;
	struct _ctrie_ *T[64];
	struct _ctrie_ *U;
	LIST_t	*L;
	int		pushed;
} CTRIE_t;


typedef enum _push_trigger_ {
	Always = 1,
	Ignore,
	Merge,
	Timer
} PSHTRIG;


typedef enum _rule_type_ {
	ADDVSERVER = 1,
	ADDSERVICE,
	SETVSERVER,
	SETSERVICE,
	BINDVSERVER,
	BINDSERVICE,
	ADDCIPHERGRP,
	BINDCIPHERGRP
} RULETYPE;


struct _set_attrib_;

typedef struct _ciphergroup_ {
	int					idx;
	int					dynamic;
	char				name[128];
	char				cipher[128][64];
	struct _ciphergroup_ *next;
} CIPHERGROUP_t;


typedef	struct _vserver_ {
	int					isVserver;
	int					isInternal;
	int					cipherIdx;
	char				name[128];
	char				type[32];
	char				cipher[128][64];
	char				ciphergroup[64];
	int					hash;
	struct _set_attrib_	*attr;
	CTRIE_t				*cur_trie;
	CIPHERGROUP_t		*cgp;
	int					ecc_curve;
	struct _vserver_ 	*next;
}VSERVER_t;


typedef	struct _service_ {
	int					isVserver;
	char				name[128];
	char				cipher[128][64];
	char				ciphergroup[64];
	struct _set_attrib_	*attr;
	CIPHERGROUP_t		*cgp;
	CTRIE_t				*cur_trie;
	struct _service_ 	*next;
}SERVICE_t;



typedef union 
{
	unsigned int flag;
	struct _param_bits_ 
	{
	unsigned int		_denySSLReneg :1;
	unsigned int		_dropReqWithNoHostHeader :1;
	unsigned int		_encryptTriggerPktCount :1;
	unsigned int		_insertionEncoding :1;
	unsigned int		_pushEncTriggerTimeout :1;
	unsigned int		_pushFlag :1;
	unsigned int		_quantumSize :1;
	unsigned int		_sendCloseNotify :1;
	unsigned int		_sslTriggerTimeout :1;
	unsigned int		_strictCAChecks :1;
	} param_bits;
}_P;


typedef struct  _ssl_params_ {
	_P		P;

	struct _param_core_ 
	{
	char				*denySSLReneg;
	unsigned int		dropReqWithNoHostHeader;
	unsigned int		encryptTriggerPktCount;
	char 				*insertionEncoding;
	unsigned int		pushEncTriggerTimeout;
	unsigned int		pushFlag;
	unsigned int		quantumSize;
	unsigned int		sendCloseNotify;
	unsigned int		sslTriggerTimeout;
	unsigned int		strictCAChecks;
	} param_core;

} SSL_PARAMS_t;



typedef union 
{
	unsigned int flag;
	struct _bits_ 
	{
	unsigned int		_dh						:1;
	unsigned int		_dhKeyExpSizeLimit		:1;
	unsigned int		_eRSA					:1;
	unsigned int		_sessReuse				:1;
	unsigned int		_cipherRedirect			:1;
	unsigned int		_sslv2Redirect			:1;
	unsigned int		_clientAuth				:1;
	unsigned int		_sslRedirect			:1;
	unsigned int		_redirectPortRewrite	:1;
	unsigned int		_nonFipsCiphers			:1;
	unsigned int		_ssl2					:1;
	unsigned int		_ssl3					:1;
	unsigned int		_tls1					:1;
	unsigned int		_tls11					:1;
	unsigned int		_tls12					:1;
	unsigned int		_SNIEnable				:1;
	unsigned int		_serverAuth				:1;
	unsigned int 		_sendCloseNotify		:1;
	unsigned int		_dhCount				:1;
	unsigned int		_eRSACount				:1;
	unsigned int		_sessTimeout			:1;
	unsigned int		_clearTextPort			:1;
	unsigned int		_dhFile					:1;
	unsigned int		_cipherURL				:1;
	unsigned int		_sslv2URL				:1;
	unsigned int		_commonName				:1;
	unsigned int		_dtlsProfileName		:1;
	unsigned int		_sslProfile				:1;
	unsigned int		_pushEncTrigger			:1;
	unsigned int 		_clientCert				:1;

	} bits;
}_U;

typedef struct  _set_attrib_ {
	_U		U;

	struct _core_ 
	{

	int		_dh						:1;
	int		_dhKeyExpSizeLimit		:1;
	int		_eRSA					:1;
	int		_sessReuse				:1;
	int		_cipherRedirect			:1;
	int		_sslv2Redirect			:1;
	int		_clientAuth				:1;
	int		_sslRedirect			:1;
	int		_redirectPortRewrite	:1;
	int		_nonFipsCiphers			:1;
	int		_ssl2					:1;
	int		_ssl3					:1;
	int		_tls1					:1;
	int		_tls11					:1;
	int		_tls12					:1;
	int		_SNIEnable				:1;
	int		_serverAuth				:1;
	int 	_sendCloseNotify		:1;


	int		_dhCount;
	int		_eRSACount;
	int		_sessTimeout;
	int		_clearTextPort;

	int		_ecc_curve;

	char	_dhFile[256];
	char	_cipherURL[256];
	char	_sslv2URL[256];
	char	_commonName[256];
	char	_dtlsProfileName[128];
	char	_sslProfile[128];
	char	_pushEncTrigger[8];
	char 	_clientCert[16];		//1=MANDATORY 0=OPTIONAL

	char	name[128];

	} core;

	int		maxServiceCount;
	int		curServiceIdx;
	int		maxVserverCount;
	int		curVserverIdx;

	SERVICE_t	**serviceList;
	VSERVER_t	**vserverList;
	CIPHERGROUP_t	*cgp;

	int			isVserver;
	LIST_t		*vList;
	LIST_t		*sList;

	struct _set_attrib_ *next;

} SET_ATTR_t;




typedef struct  _stmt_ {
	int			ruleType;
	char		cmd[8];
	char		module[32];
	char		entity[32];
	char		name[1024];

	SET_ATTR_t	setAttr;

} STMT_t;


typedef	int (*cmpFn)(void *,void *);



extern int	debugY();
extern int	debugL();
extern void *Malloc(int);
extern VSERVER_t	*handleAddVserver(char *type,char *name,int isVserver);
extern int	handleAddService(char *name);
extern int	handleSetVserver(char *name,SET_ATTR_t *attr,int isVserver);
//extern int	handleSetService(char *name, SET_ATTR_t *attr);
extern int	handleBindVserverCipher(char *vname,char *cname,int isVserver);
extern int	handleBindVserverECCCurve(char *vname,char *curve,int isVserver);
//extern int	handleBindServiceCipher(char *vname,char *cname);
extern int	handleAddCipherGroup(char *gname);
extern int	handleAddCipherGroupOld(char *gname,char *cname);
extern int	handleSSLParams(SSL_PARAMS_t *);
extern int	handleBindCipherGroup(char *gname,char *cname);
extern int	cmpAttribs(SET_ATTR_t *a, SET_ATTR_t *b);

extern CIPHERGROUP_t	*findCipherGroup(char *name);
extern VSERVER_t   		*findVserver(char *name,int isVserver);
//extern VSERVER_t   		*findService(char *name);
extern SET_ATTR_t  		*findMatchingAttr(SET_ATTR_t *a,int isVserver);
extern int addAttrVserver(SET_ATTR_t *attr, VSERVER_t *v);
extern int addAttrService(SET_ATTR_t *attr, SERVICE_t *s);

extern int writeProfile(SET_ATTR_t *a,char * buf);
extern int getNameToIndex(char *name);
extern CTRIE_t *addNameToTrie(char *name,CTRIE_t *trie);
extern int	setTrieName(char *name,CTRIE_t *trie);
extern int	initList(LIST_t *l,int num);
extern int	addToList(LIST_t *l, void *v);
extern int	freeList(LIST_t *l);
extern int	isAliasName(char *name);
extern LIST_t	*TrieToList(CTRIE_t *t);
extern CIPHERGROUP_t *listToDynamicCipherGroup(char *grpName,LIST_t *L);
extern int	reInitList(LIST_t *l);
extern CIPHERGROUP_t	*AddAliasCipherGroup(char *grpName);
extern int PrintToDynamicCipherGroup();
extern int	sortList(LIST_t *L, cmpFn fn);
extern int	vserverCipherGrpCmp(void *v1, void *v2);
extern SET_ATTR_t	*cloneAttr(SET_ATTR_t *attr);
extern SET_ATTR_t	*NewAttr(SET_ATTR_t *attr);
extern int	freeAttr(SET_ATTR_t *a);
extern int	NameDynamicCipherGroup();
extern int	PrintConfig();
extern int  PrintACipherGroup(CIPHERGROUP_t *);
extern int  PrintAProfile(SET_ATTR_t *);
extern int  PrintBoundProfiles();
extern int  PrintOneBoundProfile(SET_ATTR_t *);
extern int	getNextProfileName(char *name);
extern int	getNextCipherGroupName(char *name);
extern int	ashoke_debug();
extern int	DumpAttr(SET_ATTR_t *a);
extern int	DumpAttrList(SET_ATTR_t *alist);
