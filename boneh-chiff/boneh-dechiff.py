#python modules
import hashlib
import binascii
import os
import random
import binascii

#general modules written by myself
import modular
import ellipticCurveMod
import ellipticCurve
import finiteField
import polynomial
import WeilPairing
#if we want to work of fields different than Z/pZ
FiniteField = finiteField.FiniteField
Polynomial = polynomial.Polynomial
ModifWeil = WeilPairing.ModifWeilPairing
EllipticCurve2=ellipticCurve.EllipticCurve
Point2=ellipticCurve.Point

#if we want to work only over the field Z/pZ
EllipticCurve=ellipticCurveMod.EllipticCurve
Point=ellipticCurveMod.Point
Infinity=ellipticCurveMod.Infinity
ModP = modular.ModP

#second hash function: input an element of order l in Fp^2 and outputs a string of length n
#where the length of the message is n
def hash3 (value, lengthMessage):
	sum = 0
	#sum the coefficients
	for i,a in enumerate(value.poly):
		sum = sum + a
	value = sum.n
	
	length = lengthMessage

	#Knuth's multiplicative method:
	hash = value * 2654435761 % (2**32)
	hash = bin(hash)
	hash = hash + hash[2:] + hash[2:] + hash[2:] + hash[2:] + hash[2:]
	hash = hash[:length]
		
	output = bytearray(hash.encode())

	return output

#xor function: bitwise addition	
def xor (a,b):
	c = bytearray(len(a))
	for i in range(len(a)):
		c[i] = a[i] ^ b[i]
	return c

	
	
	
l = 56453

#p = 338717

p = int(6 * l - 1)

Fp2 = FiniteField(p,2, Polynomial([ModP(1,p),ModP(1,p),ModP(1,p)],p)) #for l=56453

E2 = EllipticCurve2( Fp2([0]), Fp2([1]), Fp2)

b = Fp2([0,1])

DIDCordX = input("Enter the X-coordinate for the Point DID as an integer: ")

DIDCordY = input("Enter the Y-coordinate for the Point DID as an integer: ")

cypherACordX = 240099

cypherACordY = 283222





print("-------------------------------")
print("Decryption")

DID = Point2(E2, Fp2([DIDCordX]), Fp2([DIDCordY]))
cypherA = Point2(E2, Fp2([cypherACordX]), Fp2([cypherACordY]))

cypherB = input("Enter the encrypted message, which you want to decrypt: ")
cypherB = binascii.unhexlify(cypherB)

length = len(cypherB)


print("The first value of the cyphertext is:")
print(cypherA)

hID = ModifWeil(DID, cypherA, l , b)

print("hID is equal to:")
print(hID)

hash = hash3(hID, length)

print("The decrypted message is:")
c = xor(cypherB , hash)
print(c.decode())