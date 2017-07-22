import fractions
import itertools
import modular
import random
import polynomial
import os

generateIrrduciblePolynomial = polynomial.generateIrrduciblePolynomial
ModP = modular.ModP
Polynomial = polynomial.Polynomial

#one can fix a polynomialModulus if you define a finite field
#however, it needs to be irreducible
def FiniteField(p, m, polynomialModulus=None):
		
	#generates a random irreducible polynomial
	#not very good for Test purposes! because always 
	#new examples will appear randomly
	if polynomialModulus is None:
		polynomialModulus = generateIrrduciblePolynomial(p, m)
		
	class Fq(object):
		fieldsize = int(p**m)
		primeSubfield = p
		idealGenerator = polynomialModulus
        
		
		def __init__(self, poly):
           
			if type(poly) is Fq:
				self.poly = poly.poly 
			elif type(poly) is int:
				self.poly = Polynomial([ModP(poly,p)],p)
			elif isinstance(poly, ModP):
				self.poly = Polynomial([ModP(poly.n,p)],p)
			elif isinstance(poly, Polynomial):
				self.poly = poly % polynomialModulus
			else:
				self.poly = Polynomial([ModP(x,p) for x in poly],p) % polynomialModulus
				
			self.field = Fq
			
		def __add__(self, other):
			return Fq(self.poly + other.poly)
			
		def __sub__(self, other):
			return Fq(self.poly - other.poly)
		
		def __mul__(self, other):
			return Fq(self.poly * other.poly)
			
		def __eq__(self, other):
			return isinstance(other, Fq) and self.poly == other.poly 
			
		#fast polynomial multiplication	
		def __pow__(self,n):
			x = self
			r = Fq([1])
			while n != 0:
				if n % 2 == 1:
					r = r * x
					n = n - 1
			
				x = x * x
				n = n / 2
				
			return Fq(r.poly)
			
		def __neg__(self):
			return Fq(-self.poly)
			
		def __abs__(self):
			return abs(self.poly)
			
		def __repr__(self):
			return repr(self.poly) + ' over ' + self.__class__.__name__
			
		def __divmod(self, divisor):
			q, r = divmod(self.poly , divisor.poly)
			return (Fq(q), Fq(r))
		
		#inverse of an element
		def inverse(self):
			if self == Fq(0):
				raise ZeroDivisionError
				
			x,y,d = extentedEuclideanAlgorithm(self.poly, self.idealGenerator)
			return Fq(x) * Fq(d.coefficients[0].inverse())
			
		#dividing
		def __div__(self,other):
			return self * other.inverse()
		
		#dividing
		def __truediv__(self, other):
			return self * other.inverse()
			
		#dividing
		def __rdiv__(self,other):
			return self * other.inverse()
		#dividing
		def __rtruediv__(self, other):
			return self * other.inverse()
		
	Fq.__name__ = 'F_{%d^%d}' % (p,m)
	return Fq
	
	
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