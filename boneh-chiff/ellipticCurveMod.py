import modular

ModP = modular.ModP

#to understand the concept behind these conditions, check the documentation 
#of elliptic curve in my bachelor thesis
class EllipticCurve(object):
	def __init__(self,a,b):
		#this construction only works for the weierstrass form
		# y^2 = x^3 + a*x + b
		self.a = a
		self.b = b
		self.p = self.a.p
		
		#compute the discriminant to check whether there are multiple roots or not
		self.discriminant = ModP(4,self.p)*a*a*a+ ModP(27,self.p)*b*b
	
		#if the curve has multiple roots, then we have to raise an exception
		#we do not want to work with curves with multiple roots
		if self.isSingular():
			raise Exception("The curve %s has multiple roots. Bad choice!" % self)
	
	#function to check if there are multiple roots
	def isSingular(self):
		# if the discriminant is zero, the method returns true
		# thus, there are multiple roots
		return self.discriminant == ModP(0,self.p)
	
	#function to check whether a point is on the curve or not
	def isPoint(self, x,y):
		# enter the coordinates of the point into the equation of the curve
		# return true if the point is on the curve
		# int cast necessary to prevent wrong multiplication as: 1*1*1 = 3 ... (yes, this happened)
		x1 = int(x.n)
		y1 = int(y.n)
		a1 = int(self.a.n)
		b1 = int(self.b.n)
		return (ModP(y1*y1,x.p)) == (ModP(x1*x1*x1 + a1 * x1 + b1,x.p))
	
	#define the string for a elliptic curve to print it properly
	def __str__(self):
		return "y^2=x^3+ %Gx+ %G" % (self.a.n, self.b.n)
		
	#check whether two elliptic curves are equal or not
	def __eq__(self, other):
		return (self.a, self.b) == (other.a, other.b)
		
		
#class for a point on the elliptic curve (!)
class Point(object):
	#we need to take the curve as an argument, because we immediately check 
	#if the point is on the curve or not
	def __init__(self, curve, x, y):
		self.curve = curve
		self.x = x
		self.y = y
		self.p = self.x.p
		
		#if the point is not on the curve, we do not need to create the point
		if not self.curve.isPoint(x,y):
			raise Exception("The point %s is not on the curve %s" % (self, self.curve))
			
	#function to output the point
	def __str__(self):
		return "(%s,%s)" % (self.x,self.y)
		
	#the negative/opposite point P s.t. P-P=infinity
	def __neg__(self):
		return Point(self.curve, self.x, -self.y)
		
	#we are going to define the addition of two points, check documentation
	def __add__(self, P):
		#if no point, the addition does not make sense
		if isinstance(P, Infinity):
			return self
			
		if (self.x, self.y) == (P.x, P.y) :
			if self.y == ModP(0,self.p):
				return Infinity(self.curve)
			
			else:
				m = ( ModP(3,self.p) * self.x * self.x + self.curve.a ) / ( ModP(2,self.p) * self.y )
				p = m * m - ModP(2,self.p) * self.x
				q = m * ( self.x - p ) - self.y
				return Point(self.curve, p ,q)
			
		else:
			if self.x == P.x:
				return Infinity(self.curve)
				
			else:
				m = (P.y - self.y) / (P.x - self.x)
				p = m*m - self.x - P.x
				q = m*(self.x - p) - self.y
				return Point(self.curve, p, q)
	
	#method for subtracting
	def __sub__(self, P):
		#adding with a negative point
		return self + -P

	#adding a point several times to itself
	def __mul__(self, n):
		#if not an integer, does not make sense
		if not isinstance(n, int):
			raise Exception("You need to input an integer")
		
		else:
			#if zero times, it results infinity
			if n == 0:
				return Infinity(self.curve)
				
			if n == 1:
				return self
			
			#if negative integer, adding the negative point n times
			if n < 0:
				return -self * -n
			
			else:
				#double-and-add algorithm for faster addition
				#not in binary, might change that later
				#http://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
				P = self
				Q = Infinity(self.curve)
				
				while n > 0:
				
					if (n % 2) == 1:
						Q = P + Q
						n = n-1
					else:
						P = P + P
						n = n / 2		
				return Q
				
	def __rmul__(self, n):
		return self * n
		
	def __eq__(self, other):
		if isinstance(self, Infinity) and isinstance(other, Infinity):
			return True
		if isinstance(self, Infinity) and not isinstance(other, Infinity):
			return False
		if not isinstance(self, Infinity) and isinstance(other, Infinity):
			return False
		if self.x == other.x and self.y == other.y and self.p == other.p:
			return True
		
#general remark: we always have integer < string
class Infinity(Point):
	def __init__(self,curve):
		self.curve = curve
		#the infinity point is always on the curve
	
	#maybe I will change the notation to make it look more mathematically
	def __str__(self):
		return "Infnity"
		
	#stays the same, because neutral element
	def __neg__(self):
		return self
		
	#infinity is neutral element
	def __add__(self, P):
		return P
		
	#infinity is neutral element
	def __sub__(self,P):
		return P
	
	#adding infinity n times to itself
	def __mul__(self, n):
		#if not integer, doesnt make sense
		if not isinstance(n, int):
			raise Exception("You need to input an integer")
		
		else:
			return self
	
	
#there is an explanation of the algorithm in my thesis
def MillerFunction(P, R, Q):	
	
	if isinstance(P, Infinity) or isinstance(R, Infinity):
		if P == R:
			return ModP(1, Q.p)
		if isinstance(P, Infinity):
			return Q.x - R.x
		if isinstance(R, Infinity):
			return Q.x - P.x
			
	else:
		if P != R:
			if P.x == R.x:
				return Q.x - P.x
			else:
				l = ( R.y - P.y ) / (R.x - P.x)
				return Q.y - P.y - l * (Q.x - P.x)
		else:
			numerator = ModP(3, P.p) * (P.x * P.x) + P.curve.a
			denominator = ModP(2, P.p) * P.y
			if denominator == ModP(0, P.p):
				return Q.x - P.x
			else:
				l = numerator / denominator
				return Q.y - P.y - l * (Q.x - P.x)



def Miller(P, Q, m):
	t = ModP(1,P.p)
	V = P
	S = 2*V
	mylist = list(bin(m)[2:])
	i = 1
	while i < len(mylist):
		S = 2*V
		t = (t*t)*(MillerFunction(V,V,Q) / MillerFunction(S,-S,Q))
		V = S
		if mylist[i] == '1':
			S = V + P
			t = t * (MillerFunction(V,P,Q) / MillerFunction(S,-S,Q))
			V = S
		i = i + 1
	return t


def WeilPairing(P,Q,m):
	if not isinstance(m*P, Infinity) or not isinstance(m*Q, Infinity):
		raise Exception("The two points do not have order %d" %m)
	if P == Q:
		return ModP(1,P.p)
	if isinstance(P, Infinity) or isinstance(Q, Infinity):
		return ModP(1, P.p)
	fmPQ = Miller(P,Q,m)
	fmQP = Miller(Q,P,m)
	if fmQP == ModP(0, P.p):
		return ModP(1, P.p)	
	return (ModP((int(-1))**(m),P.p))*(fmPQ / fmQP)
	











