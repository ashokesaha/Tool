from	TestException	import *
from	test_dut		import *
from	test_util		import *


class	BaseTest(object) :
	desc = "This is a test for .."
	TestList = []
	TestSession  = None

	def __init__(self, nsip) :
		self.nsip = nsip

	def	Setup(self) :
		SetupFn(self)	


	def	Start(self) :
		StartFn(self)	


	@classmethod
	def About(cls) :
		return cls.desc

	@classmethod
	def	RegisterTest(cls,t) :
		if not isinstance(t,BaseTest) :
			raise TestException(1)
		cls.TestList.append(t)




def	SetupFn(bt) :
	print 'this is SetupFn of BaseTest'
	pass

def	StartFn(bt) :
	bt.TestSession = Login(bt.nsip)
	d = GetIPS(bt.TestSession)


