#!/usr/bin/env python

import kalk


x = kalk.Variable("x")

expo = kalk.ExponentTerm(x,kalk.Constant(5))
abi = kalk.AbsoluteTerm(expo) #  |x**5|

nega = kalk.NegationTerm(kalk.Constant(2))
muli = kalk.MultiplicationTerm(abi,nega) # |x**5| * (-2)

myTerm = kalk.AdditionTerm(muli,x) # (|x**5| * (-2)) + x
#print ("Redu: "+str(reduction))
#print(myTerm.solve({x:5}))
#print("Reduced Derivate: "+str(reduced_derivation))

print(myTerm)
print()
print(myTerm.makeTree())

#print()
reduction = myTerm.reduce()
print()
print(reduction.makeTree())

#x5 = {x:5}
#print(myTerm.solve(x5))
#print(reduction.solve(x5))