#!/usr/bin/python

class _Term:
	#you solve a Term by applying the functions
	#and reducing variables to constants, which in turn become actual numbers
	def solve(self,solvents):
		pass
	def __str__(self):
		return ""
	def derive(self,var):
		assert(isinstance(var,Variable))
	def makeTree(self):
		retu = self._makeTree("")
		assert(type(retu) == str)
		return retu
	def _makeTree(self,prefix):
		return ""

class _UnaryTerm(_Term):
	def __init__(self,arg):
		self._operatorSign = "?"
		assert(isinstance(arg,_Term))
		self.mid = arg
	def __str__(self):
		return self._operatorSign + str(self.mid)
	def reduce(self):
		return self.mid.reduce()
	def _makeTree(self,prefix):
		retu = self._operatorSign
		retu += self.mid._makeTree(prefix+" ")
		assert(type(retu) == str)
		return retu

#lhs: left  hand side argument
#rhs: right hand side argument
#as rule: lhs argument ALWAYS first and rhs argument ALWAYS second
class _BinaryTerm(_Term):
	def __init__(self,lhsArg,rhsArg):
		self._operatorSign = "?"
		assert(isinstance(rhsArg,_Term) and isinstance(lhsArg,_Term))
		self.rhs = rhsArg
		self.lhs = lhsArg
	def __str__(self):
		return str(self.lhs)+self._operatorSign+str(self.rhs)
	def reduce(self):
		nl = self.lhs.reduce()
		assert(nl != None)
		nr = self.rhs.reduce()
		assert(nr != None)
		return (nl,nr)
	def _makeTree(self,prefix):
		left = self._operatorSign
		left += self.lhs._makeTree(prefix+"┃")
		right = prefix + "┖"
		right += self.rhs._makeTree(prefix+" ")
		return left + "\n" + right




class Constant(_Term):
	def __init__(self,c):
		assert(type(c) in [int,float])
		self.val = c
	def solve(self,solvents):
		return self.val
	def __str__(self):
		return str(self.val)
	def derive(self,var):
		return Constant(0)
	def reduce(self):
		return Constant(self.val)
	def _makeTree(self,depth):
		return str(self.val)

class Variable(_Term):
	def __init__(self,n):
		assert(type(n) == str)
		self.name = n
	def __str__(self):
		return self.name
	def solve(self,solvents):
		assert(solvents != None)
		assert(self in solvents.keys())
		return solvents[self]
	def derive(self,var):
		if(var is self):
			return Constant(1)
		else:
			return Constant(0)
	def reduce(self):
		return self
	def _makeTree(self,depth):
		return self.name



class NegationTerm(_UnaryTerm):
	def __init__(self,c):
		_UnaryTerm.__init__(self,c)
		self._operatorSign = "-"
	def solve(self,solvents):
		return - self.mid.solve(solvents)
	def derive(self,var):
		return NegationTerm(self.mid.derive(var))
	def reduce(self):
		retu = super(NegationTerm,self).reduce()
		if(isinstance(retu, Constant)):
			return Constant(-retu.val)
		else:
			return retu
	def _makeTree(self,prefix):
		retu = " " + super(NegationTerm,self)._makeTree(prefix+" ")
		return retu

class AbsoluteTerm(_UnaryTerm):
	def __init__(self,c):
		assert(isinstance(c,_Term))
		_UnaryTerm.__init__(self,c)
		self._operatorSign = "abs"
	def solve(self,solvents):
		return abs( self.mid.solve(solvents))
	def __str__(self):
		return "|"+str(self.mid)+"|"
	def derive(self,var):
		return AbsoluteTerm(self.mid.derive(var))
	def reduce(self):
		retu = super(AbsoluteTerm,self).reduce()
		if(isinstance(retu,AbsoluteTerm) or
			isinstance(retu,NegationTerm)):
			return AbsoluteTerm(retu.mid)
		elif(isinstance(retu,Constant) and
				retu.val < 0):
			return Constant(retu.val*(-1))
		else:
			return AbsoluteTerm(retu)
	def _makeTree(self,prefix):
		return "|"+self.mid._makeTree(prefix+"|")


class AdditionTerm(_BinaryTerm):
	def __init__(self,lhs,rhs):
		_BinaryTerm.__init__(self,lhs,rhs)
		self._operatorSign = "+"
	def solve(self,solvents):
		return self.lhs.solve(solvents) + self.rhs.solve(solvents)
	def derive(self,var):
		return AdditionTerm(self.lhs.derive(var),self.rhs.derive(var))
	def reduce(self):
		retu = super(AdditionTerm,self).reduce()
		if(type(retu) == tuple):
			if(isinstance(retu[0],Constant) and
				isinstance(retu[1],Constant)):
				return Constant(retu[0].val + retu[1].val)
			else:
				return AdditionTerm(retu[0],retu[1])
		else:
			return retu
		#todo if one is a negation, you can make a subtraction out of it



class SubtractionTerm(_BinaryTerm):
	def __init__(self,lhs,rhs):
		_BinaryTerm.__init__(self,lhs,rhs)
		self._operatorSign = "-"
	def solve(self,solvents):
		return self.lhs.solve(solvents) - self.rhs.solve(solvents)
	def derive(self,var):
		return SubtractionTerm(
			self.lhs.derive(var),
			self.rhs.derive(var))
	def reduce(self):
		retu = super(SubtractionTerm,self).reduce()
		if(type(retu) == tuple):
			if(isinstance(retu[0],Constant) and
				isinstance(retu[1],Constant)):
				return Constant(retu[0].val - retu[1].val)
			else:
				return SubtractionTerm(retu[0],retu[1])
		else:
			assert(isinstance(retu,_Term))
			return retu

class MultiplicationTerm(_BinaryTerm):
	def __init__(self,lhs,rhs):
		_BinaryTerm.__init__(self,lhs,rhs)
		self._operatorSign = "*"
	def solve(self,solvents):
		return self.lhs.solve(solvents) * self.rhs.solve(solvents)
	def derive(self,var):
		return AdditionTerm(
			MultiplicationTerm(self.lhs,self.rhs.derive(var)),
			MultiplicationTerm(self.rhs.derive(var),self.lhs))
	def reduce(self):
		retu = super(MultiplicationTerm,self).reduce()
		#print(retu)
		if(type(retu) == tuple):
			if(isinstance(retu[0],Constant) and retu[0].val == 0):
					return Constant(0)
			elif(isinstance(retu[1],Constant) and retu[1].val == 0):
					return Constant(0)
			else:
				return MultiplicationTerm(retu[0],retu[1])
		assert(type(retu) != tuple)
		print(type(retu))
		assert(isinstance(retu,_Term))
		return retu

#lhs: dividend / numerator
#rhs: divisor  / denominator
class DivisionTerm(_BinaryTerm):
	def __init__(self,lhs,rhs):
		_BinaryTerm.__init__(self,lhs,rhs)
		self._operatorSign = "/"
	def solve(self,solvents):
		return float(self.rhs.solve(solvents)) / float(self.lhs.solve(solvents))
	def derive(self,var):
		return DivisionTerm(
			SubtractionTerm(
				MultiplicationTerm(
					self.lhs.derive(var),
					self.rhs),
				MultiplicationTerm(
					self.lhs,
					self.rhs.derive(var))
				),
			ExponentTerm(self.rhs,Constant(2))
			)

#rhs argument is always exponent
class ExponentTerm(_BinaryTerm):
	def __init__(self,lhs,rhs):
		_BinaryTerm.__init__(self,lhs,rhs)
		self._operatorSign = "^"
	def solve(self,solvents):
		return self.lhs.solve(solvents) ** self.rhs.solve(solvents)
	def derive(self,var):
		#assert()
		return MultiplicationTerm(
			self.rhs, ExponentTerm(
				self.lhs,
				SubtractionTerm(self.rhs, Constant(1))
				)
			)
	def reduce(self):
		super(ExponentTerm,self).reduce()
		if(isinstance(self.rhs,Constant)):
			if(self.rhs.val == 0):
				return Constant(1)
		return self


