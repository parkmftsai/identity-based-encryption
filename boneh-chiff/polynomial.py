import fractions
import itertools
import modular
import random

ModP = modular.ModP

#strip all copies of eraseValue of the end of the list
#i.e. erase all 0 at the end (in our case)
def strip(L, eraseValue):
	if len(L) == 0:
		return L
		
	i = len(L)-1
	
	while i>=0 and L[i] == eraseValue:
		i = i-1

	return L[:i+1]

	
#define polynomaials under the form of:
#a + b*x + c*x^2 + ...
class Polynomial(object):	
	def __init__(self, c, p):
		if type(c) is Polynomial:
			self.coefficients = c.coefficients
		elif isinstance(c, ModP):
			self.coefficients = [c]
		elif not hasattr(c, '__iter__') and not hasattr(c, 'iter'):
			self.coefficients = [ModP(c,p)]
		else:
			self.coefficients = c
		
		self.p = p
		self.coefficients = strip(self.coefficients, ModP(0,p))
		self.name = '(Z/%dZ)[x]' % p
		
	
	#check if the polynomial is 0
	def isZero(self):
		return self.coefficients == []
	
	#function to print the polynomial
	def __repr__(self):
		if self.isZero():
			return '0'
		#iterate through the list of coefficients and add them to one string
		else:
			return  ' + '.join(['%s x^%d' % (a,i) if i>0 else '%s' % a for i,a in enumerate(self.coefficients)])
	
	#length of the polynomial
	def __abs__(self):
		return len(self.coefficients)
		
	#length of the polynomial
	def __len__(self):
		return len(self.coefficients)
		
	#subtract to polynomials by subtracting their coeff.
	def __sub__(self, other):
		return self + (-other)
		
	def __rsub__(self, other):
		return -self + other
		
	#iterate through the coefficients
	def __iter__(self):
		return iter(self.coefficients)
		
	#negative of a polynomial
	def __neg__(self):
		return Polynomial([-a for a in self],self.p)
		
	#iterate through polynomial
	def iter(self):
		return self.__iter__()
		
	#the leading coefficient of a polynomial
	def leadingCoefficient(self):
		return self.coefficients[-1]
	
	#the degree of a polynomial, ie largest exponent
	def degree(self):
		return abs(self)-1
		
	#check whether two polynomials are equal or not by comparing coefficients and same degree
	def __eq__(self,other):
		return  self.degree() == other.degree() and all([x==y for (x,y) in zip (self,other)])
		
	#add two polynomials by adding their coefficients
	def __add__(self,other):
		#if integer, than one needs to make a constant polynomial
		if isinstance(other, int):
			other = Polynomial([other],self.p)
		#adding the coefficients together. fillvalue defines the value to use if one polynomial
		#has a smaller degree than the other one.
		newCoefficients = [sum(x) for x in itertools.zip_longest(self,other, fillvalue = ModP(0,self.p))]
		return Polynomial(newCoefficients, self.p)
		
	def __radd__(self, other):
		return self + other
		
	#multiplication of two polynomials
	def __mul__(self,other):
		if isinstance(other, int):
			return self*Polynomial([other],self.p)
		if self.isZero() or other.isZero():
			return Zero(self.p)
		else:
			#set all coefficients to zero
			newCoefficients = [ModP(0,self.p) for _ in range(len(self) + len(other) - 1)]
			
			#general formula for the coefficients of the multiplication of two poly.
			for i,a in enumerate(self):
				for j,b in enumerate(other):
					newCoefficients[i+j] = newCoefficients[i+j] + a*b
					
			return Polynomial(newCoefficients,self.p)
			
	def __rmul__(self, other):
		return self * other
				
	#divmod for polynomials
	def __divmod__(self,divisor):
		quotient = Zero(self.p)
		remainder = self
		divisorDeg = divisor.degree()
		divisorLC = divisor.leadingCoefficient()
		
		while remainder.degree() >= divisorDeg:
			StockExponent = remainder.degree() - divisorDeg
			StockZero = [ModP(0,self.p) for _ in range(StockExponent)]
			StockDivisor = Polynomial(StockZero + [remainder.leadingCoefficient() / divisorLC], self.p)
			
			quotient = quotient + StockDivisor
			remainder = remainder - (StockDivisor * divisor)
		
		return quotient, remainder
		
	#modular function for polynomials
	def __mod__(self, divisor):
		x,y = divmod(self, divisor)
		return y

	def __pow__(self, p):
		x = self
		r = Polynomial(1,self.p)
		while p != 0:
			if p % 2 == 1:
				r = r * x
				p = p - 1
			
			x = x * x
			p = p / 2
		return r	
			
	#polynomial to the power p modulo other
	def powmod(self, p, other):
		x,y = divmod(self**p, other)
		return y
		
	#usual division
	def __truediv__(self, divisor):
		if divisor.isZero():
			raise ZeroDivisionError
		x,y = divmod(self, divisor)
		return x
		
	#usual division
	def __div__(self, other):
		return self.__truediv__(other)
		
	

#returns a Zero polynomial
def Zero(p):
		return Polynomial([],p)
		
#check whether a polynomial is irreducible or not
def isIrreducible(polynomial, p):
	#polynomial "x"
	x = Polynomial([ModP(0,p), ModP(1,p)],p)
	powerTerm = x
	isUnit = lambda p: p.degree() == 0;
		
	for _ in range( int(polynomial.degree() / 2)):
		powerTerm = powerTerm.powmod(p, polynomial)
		gcdOverZmodp = gcd(polynomial, powerTerm - x)
		if not isUnit(gcdOverZmodp):
			return False
		
	return True
	
#greatest common divisor
def gcd(a,b):
	if abs(a) < abs(b):
		return gcd(b,a)
		
	while abs(b) > 0:
		q,r = divmod(a,b)
		a,b = b,r
		
	return a
	
#returns an irreducible polynomial
def generateIrrduciblePolynomial(p, degree):
		
	while True:
		coefficients = [ModP(random.randint(0, p-1),p) for _ in range(degree)]
		randomMonicPolynomial = Polynomial(coefficients + [ModP(1,p)],p)
			
		if isIrreducible(randomMonicPolynomial, p):
			return randomMonicPolynomial
			
				
def extentedEuclideanAlgorithm(a, b):
	if abs(b) > abs(a):
		(x,y,d) = extentedEuclideanAlgorithm(b,a)
		return (y,x,d)
		
	if abs(b) == 0:
		return (1,0,a)
		
	x1, x2, y1, y2 = 0,1,1,0
	while abs(b) > 0:
		q, r = divmod(a,b)
		x = x2 - q*x1
		y = y2 - q*y1
		a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y 
		
	return (x2, y2, a)
				