from	BaseTest		import	*
from	TestSSLService	import	*

class	TestOne(BaseTest) :
	desc = "This is TestOne\n"\
                "1 2 3"
	
	def	Start(self) :
		super(TestOne,self).Start()
		StartFn(self)


	def	Setup(self) :
		super(TestOne,self).Setup()
		SetupFn(self)





def	SetupFn(self) :
	pass



def	StartFn(bt) :
	sG = Gen_SSLBESvc(count=5)
	bt.svcList = [svc for svc in sG]


to = TestOne('10.102.28.201')
to.Start()
