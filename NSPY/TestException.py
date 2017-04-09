
class	TestException(Exception) :

	Errors = {
		0 	: 'Success',
		1 	: 'Failure',
		100 : 'No Session with DUT ',
		101 : 'SNIP not present ',
		102 : 'VIP  not present ',
		103 : 'NSIP not present '
	}

	def __init__(self,code=0) :
		print 'TestException with error {}'.format(code)
		self.ecode = code 
		self.emsg  = self.__class__.Errors[self.ecode]

	def	message(self) :
		return self.emsg


