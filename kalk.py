#!/usr/bin/python

class _Term:
	#you solve a Term by applying the functions
	#and reducing variables to constants, which in turn become actual numbers
	def solve(self,solvents):
		pass
	def toString(self):
		return ""
	def derive(self,var):
		assert(isinstance(var,Variable))

class _UnaryTerm(_Term):
	def __init__(self,arg):
		self._operatorSign = "?"
		assert(isinstance(arg,_Term))
		self.mid = arg
	def toString(self):
		return self._operatorSign + self.mid.toString()

#lhs: left  hand side argument
#rhs: right hand side argument
#as rule: lhs argument ALWAYS first and rhs argument ALWAYS second
class _BinaryTerm(_Term):
	def __init__(self,lhsArg,rhsArg):
		self._operatorSign = "?"
		assert(isinstance(rhsArg,_Term) and isinstance(lhsArg,_Term))
		self.rhs = rhsArg
		self.lhs = lhsArg
	def toString(self):
		return self.lhs.toString() + self._operatorSign + self.rhs.toString()




class Constant(_Term):
	def __init__(self,c):
		assert(type(c) in [int,float])
		self.val = c
	def solve(self,solvents):
		return self.val
	def toString(self):
		return str(self.val)
	def derive(self,var):
		return 0

class Variable(_Term):
	def __init__(self,n):
		assert(type(n) == str)
		self.name = n
	def toString(self):
		return self.name
	def solve(self,solvents):
		assert(self in solvents.keys())
		return solvents[self]
	def derive(self,var):
		if(var is self):
			return Constant(1)
		else:
			return Constant(0)



class NegationTerm(_UnaryTerm):
	def __init__(self,c):
		_UnaryTerm.__init__(self,c)
		self._operatorSign = "-"
	def solve(self,solvents):
		return - self.mid.solve(solvents)
	def derive(self,var):
		return NegationTerm(self.mid.derive(var))


class AdditionTerm(_BinaryTerm):
	def __init__(self,lhs,rhs):
		_BinaryTerm.__init__(self,lhs,rhs)
		self._operatorSign = "+"
	def solve(self,solvents):
		return self.lhs.solve(solvents) + self.rhs.solve(solvents)
	def derive(self,var):
		return AdditionTerm(self.lhs.derive(var),self.rhs.derive(var))

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




x = Variable("x")
myTerm = ExponentTerm(x,Constant(3))
print(myTerm.toString())
print(myTerm.solve({x:5}))
derivation = myTerm.derive(x)
print(derivation.toString())