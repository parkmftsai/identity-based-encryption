#creating a class for being able to represent finite fields
# for instance: 7 (mod 11)
class ModP (object):
	def __init__(self, n, p):
		#prime number p for (mod p)
		self.p = int(p)
		#class of n in (mod p)
		self.n = int(int(n) % p) 
		#name of the field
		self.name = "Z/%dZ" % p
			
	#method for adding two elements of the same field
	def __add__(self, other):
		if isinstance(other, int):
			return ModP(self.n + other, self.p)
		if other.p == self.p:
			return ModP(self.n + other.n, self.p)
		else: 
			raise Exception("Different fields")
			
	def __radd__(self, other):
		if isinstance(other, int):
			return self + other
		if other.p == self.p:
			return ModP(self.n + other.n, self.p)
		else: 
			raise Exception("Different fields")

	#method for subtracting two elements of the same field
	def __sub__(self, other):
		if isinstance(other, int):
			return ModP(self.n - other, self.p)
		if other.p == self.p:
			return ModP(self.n - other.n, self.p)
		else: 
			raise Exception("Different fields")
	
	#method for multiplying two elements of the same field
	def __mul__(self, other):
		if isinstance(other, int):
			other = ModP(other, self.p)
		if other.p == self.p:
			#print(self.n *other.n %  self.p)
			return ModP(self.n * other.n, self.p)
		else: 
			raise Exception("Different fields")
			
	def __rmul__(self, other):
		return self * other
	
	#method for dividing two elements of the same field
	def __truediv__(self, other):
		if isinstance(other, int):
			other = ModP(other, self.p)
		if other.p == self.p:
			return self * other.inverse()
		else: 
			raise Exception("Different fields")
		
	#method for dividing two elements of the same field
	def __div__(self, other):
		if isinstance(other, int):
			other = ModP(other, self.p)
		if other.p == self.p:
			return self * other.inverse()
		else: 
			raise Exception("Different fields")
	
	#method for getting the inverse of an element
	def __neg__(self):
		return ModP(-self.n, self.p)
			
	#check if two elements are the same
	def __eq__(self, other):
		if isinstance(other, int):
			other = ModP(other,self.p)
		return other.p == self.p and self.n == other.n
		
	#absolute value of an element
	def __abs__(self):
		return abs(self.n)
		
	#string representation
	def __str__(self):
		return "%d (mod %d)" % (self.n, self.p)
	
	#usual representation
	def __repr__(self):
		return "%d (mod %d)" % (self.n, self.p)
		
	#multiplicative inverse of an element is calculated by Euclidean Algorithm
	def inverse(self):
		g, x, y = EuclideanAlgo(self.n, self.p)
		if g != 1:
			raise ValueError
		return ModP(x, self.p)

#Euclidean Algorithm for computing the inverse of an element
#http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def EuclideanAlgo(a,b):
	lastremainder, remainder = abs(a), abs(b)
	x, lastx, y, lasty = 0, 1, 1, 0
	while remainder:
		lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
		x, lastx = lastx - quotient*x, x
		y, lasty = lasty - quotient*y, y
	return lastremainder, lastx * (-1 if a < 0 else 1), lasty * (-1 if b < 0 else 1)
	