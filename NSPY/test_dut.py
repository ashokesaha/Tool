
class	DUT(object) :
	_nsip =  None
	_vip  =  None
	_snip =  None
	_session = None

	def __init__(self):
		self._localx = 5
		pass
		
	@classmethod	
	def setNSIP(cls,nsip) :
		_nsip = nsip

	@classmethod	
	def setVIP(cls,vip) :
		_vip = vip

	@classmethod	
	def setSNIP(cls,snip) :
		_snip = snip

	@property
	def NSIP(self) :
		return self.__class__._nsip

	@NSIP.setter
	def NSIP(self,nsip) :
		self.__class__._nsip = nsip

	@property
	def VIP(self) :
		return self.__class__._vip

	@VIP.setter
	def VIP(self,vip) :
		self.__class__._vip = vip

	@property
	def SNIP(self) :
		return self.__class__._snip

	@SNIP.setter
	def SNIP(self,snip) :
		self.__class__._snip = snip

	@property
	def SESSION(self) :
		return self.__class__._session

	@SESSION.setter
	def SESSION(self,session) :
		self.__class__._session = session


