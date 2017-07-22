import ellipticCurve
import MillerAlgorithm
def WeilPairing(P,Q,m):
	field = P.curve.field
	if P == Q:
		return field([1])
	if isinstance(P, ellipticCurve.Infinity) or isinstance(Q, ellipticCurve.Infinity):
		return field([1])
	fmPQ = MillerAlgorithm.Miller(P,Q,m)
	fmQP = MillerAlgorithm.Miller(Q,P,m)
	if fmQP == field([0]):
		return field([1])
	return (field([(-1)**(m)]))*(fmPQ / fmQP)


def ModifWeilPairing(P,Q,m,b):
	if isinstance(Q, ellipticCurve.Infinity):
		return WeilPairing(P,Q,m)
	else:
		Q = ellipticCurve.Point(Q.curve, b*Q.x, Q.y)
		return WeilPairing(P,Q,m)