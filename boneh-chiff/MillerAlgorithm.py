import ellipticCurve
def MillerFunction(P, R, Q):	
	field = P.curve.field
	if isinstance(P, ellipticCurve.Infinity) or isinstance(R, ellipticCurve.Infinity):
		if P == R:
			return field([1])
		if isinstance(P, ellipticCurve.Infinity):
			return Q.x - R.x
		if isinstance(R, ellipticCurve.Infinity):
			return Q.x - P.x
			
	else:
		if P != R:
			if P.x == R.x:
				return Q.x - P.x
			else:
				l = ( R.y - P.y ) / (R.x - P.x)
				return Q.y - P.y - l * (Q.x - P.x)
		else:
			numerator = field([3]) * (P.x * P.x) + P.curve.a
			denominator = field([2]) * P.y
			if denominator == field([0]):
				return Q.x - P.x
			else:
				l = numerator / denominator
				return Q.y - P.y - l * (Q.x - P.x)



def Miller(P, Q, m):
	field = P.curve.field
	t = field([1])
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
    
	print("t:",t)
	return t








