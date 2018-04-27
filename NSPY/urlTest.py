import httplib
import json

class NSStats(object) :
    pcb_cur_alloc = None
    pcb_cur_free  = None
    ssl_cur_sslInfo_SPCBAllocCount  = None
    ssl_cur_sslInfo_SPCBFreeCount = None
    sys_cur_nsbs = None
    sys_cur_freensbs = None
    ssl_cur_sslInfo_SessionNodeAllocCount = None
    ssl_cur_sslInfo_SessionNodeFreeCount = None
    sys_cur_alloc_bm16_entries = None
    sys_cur_free_bm16_entries = None
    sys_cur_alloc_bm32_entries = None
    sys_cur_free_bm32_entries = None
    sys_cur_alloc_bm64_entries  = None
    sys_cur_free_bm64_entries = None
    sys_cur_alloc_bm128_entries  = None
    sys_cur_free_bm128_entries = None
    sys_cur_alloc_bm256_entries  = None
    sys_cur_free_bm256_entries = None
    sys_cur_alloc_bm512_entries  = None
    sys_cur_free_bm512_entries = None
    sys_cur_alloc_bm1024_entries  = None
    sys_cur_free_bm1024_entries = None
    sys_cur_alloc_bm2048_entries  = None
    sys_cur_free_bm2048_entries = None



    

    


def URLTest(ll) :
    if len(ll) == 0 :
        return
    
    Req = '/nitro/v1/stat/nsglobalcntr?args=counters:'
    h1 = httplib.HTTPConnection('10.102.28.201')
    h1.connect()
    l = ll.pop(0)
    Req += l

    for l in ll :
        Req += ';' + l
    #print Req

    h1.putrequest('GET',Req)
    h1.putheader('X-NITRO-USER','nsroot')
    h1.putheader('X-NITRO-PASS','nsroot')
    h1.endheaders()
    h1.send('')
    h2 = h1.getresponse()
    d = h2.read()
    #print d
    dd = json.loads(d)
    d = dd['nsglobalcntr']
    #print 'nsglobalcntr::'
    #print type(d)
    #print d
    s =  ':'.join(d.values())
    print s
    o = One(d)
    print o.ssl_cur_sslInfo_SPCBAllocCount
    print o.ssl_cur_sslInfo_SPCBFreeCount
    print o.sys_cur_nsbs
    print o.pcb_cur_alloc
    print o.pcb_cur_free
    
    #print o
    #print o.errorcode
    #print o.ssl_cur_sslInfo_SPCBFreeCount
    
    
    


class  One(object) :
    def __init__(self,j=None) :
        if not j :
            pass
        elif j.__class__.__name__ == 'dict' :
            self.__dict__ = j
        else :
            self.__dict__ = json.loads(j)
        


def  CTest() :
    o = NSStats()
    dd = dict((k, v) for k, v in NSStats.__dict__.iteritems())
    print dd
    del dd['__module__']
    ll = list(dd.keys())
    print ll
   

##dd = NSStats.__dict__
##ddd = dict(dd)
##del ddd['__doc__']
##del ddd['__module__']
##del ddd['__weakref__']
##
##print ddd
##print type(ddd)
##o = One(ddd)
##print o.ssl_cur_sslInfo_SPCBAllocCount



ll = ['pcb_cur_alloc','pcb_cur_free','ssl_cur_sslInfo_SPCBAllocCount',
      'ssl_cur_sslInfo_SPCBFreeCount','sys_cur_nsbs']

URLTest(ll)

