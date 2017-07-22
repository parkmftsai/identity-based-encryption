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

#if we want to work of fields different than Z/pZ
FiniteField = finiteField.FiniteField
Polynomial = polynomial.Polynomial
ModifWeil = ellipticCurve.ModifWeilPairing
EllipticCurve2=ellipticCurve.EllipticCurve
Point2=ellipticCurve.Point

#if we want to work only over the field Z/pZ
EllipticCurve=ellipticCurveMod.EllipticCurve
Point=ellipticCurveMod.Point
Infinity=ellipticCurveMod.Infinity
ModP = modular.ModP


#class to store the cyphertext
class Ciphertext (object):
	def __init__(self, a, b):
		self.a = a
		self.b = b
		
	def __str__(self):
		return "%s and %s" % (self.a, self.b)

#find a point on the elliptic curve
#starting with the y coordinate
def findPoint(C,l, p):
	i = int(3)
	while True:
		#replace y by value an find the x value
		Py = ModP(i,p)
		Px = (Py*Py-ModP(1,p))
		Px = ModP(Px.n**(1/3.0),p)
		#if a point and order correct, return it
		if C.isPoint(Px,Py):
			P = Point(C, Px, Py)
			if isinstance(P*l, Infinity):
				return P
			#6*P is of order 1 or l, check proposition
			elif isinstance(6*P*l, Infinity):
				return 6*P
		i = i + 1
		#if we tried too much possibilities, we stop the program
		if i > 300000:
			raise Exception("No point could be found")

#find a point on the elliptic curve
#starting with the x coordinate
#test have shown that in most cases this one finds faster a point
def findPoint2(C,l, p):
	i = int(3)
	while True:
		#replace x by value and find y
		Px = ModP(i,p)
		Py = (Px*Px*Px+ModP(1,p))
		
		Py = ModP((Py.n)**(1/2.0),p)
		
		#if a point and order correct, return it
		if (C.isPoint(Px,Py)):
			P = Point(C, Px, Py)
			
			if isinstance(P*l, Infinity):
				return P
			#6*P is of order 1 or l, check proposition
			elif isinstance(6*P*l, Infinity):
				print(Px.n, Py.n)
				return 6*P
		i = i + 1
		#if tried too much possibilites, try to find a point
		#by starting with y value
            
		if i > 300000:
			P = findPoint(C,l,p)
           
			return P
			
def hash (ID, C, p, Q, l):
	i = int(0)
	while True:
		#always initialize the hash function, so that both parties can find the same hashed point
		hash1 = hashlib.md5()
		hash1.update(ID.encode('utf-8'))
		#get the integer from the hash value and multiply it to the base point
		k = int.from_bytes(hash1.digest(), byteorder='big')+i
		P = Q*k
		#if point of order l, return it
		if isinstance(P*l, Infinity) and P!=Q:
			return P
			#6*P is of order 1 or l, check proposition
		elif isinstance(6*P*l, Infinity) and P!=Q:
			return 6*P
		i = i + 1
		#if no point found, try to replace y by a value and find x
		if i > 300000:
			raise Exception("No point could be found")

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
		
	output = bytearray(hash.encode('utf-8'))

	return output

#xor function: bitwise addition	
def xor (a,b):
	c = bytearray(len(a))
	for i in range(len(a)):
		c[i] = a[i] ^ b[i]
	return c
		
	

if __name__=='__main__':

    #open file to save parameters gotten
    #through this computation
    print("==-------------------------------")

    outputFile = open('parameters.txt','w')

    outputFile.write('If you are going to change the parameters in the encrypting file, you need to adapt some parameters in the decryption file'+'\n')
    outputFile.write('You will always need to adapt the coordinates of DID and you need to copy the last output line of this file to properly decrypt'+'\n')
    outputFile.write('-------------------------------'+'\n')

    print("-------------------------------")
		


    print("-------------------------------")
    print("Initializing:")
		
    #l=109
    #l=127 
    #l=199	
    #l=56453

    #defining the values for l and p of the scheme
    #l = int(127) #working!!!
    l = int(56453)
    p = int(int(6) * l - int(1))

    #define the two fields for later purpose
    #Fp = FiniteField(p,1) #for l=127
    #important to give the irreducible polynomial
    #Fp2 = FiniteField(p,2, Polynomial([ModP(6,p),ModP(758,p),ModP(1,p)],p)) #for l=127

    Fp = FiniteField(p,1) #for l=56453
    print('Fp:%d' %Fp.fieldsize)

    Fp2 = FiniteField(p,2, Polynomial([ModP(1,p),ModP(1,p),ModP(1,p)],p)) #for l=56453
    print(Polynomial([ModP(1,p),ModP(1,p),ModP(1,p)],p).coefficients)
    #define ONE third root of unity of Fp^2
    #b = Fp2([249,341]) #for l = 127
    b = Fp2([0,1]) #for l=56453

    print("The prime number l is:")
    print(l)
    outputFile.write('The prime number l is: '+str(l)+'\n')
    print("The prime number p is:")
    print(p)
    outputFile.write('The prime number p is: '+str(p)+'\n')
    print("The third root of unity is:")
    print(b)
    outputFile.write('Third root of unit is: '+str(b)+'\n')

    #condition of the scheme to work properly
    if (p-2) % 3 != 0:
	    raise Exception("p does not verifiy the condition 2 mod 3")

    print("-------------------------------")
    print("The elliptic curve is:")
    C = EllipticCurve(ModP(0,p),ModP(1,p))
    print(C)


    print("The choosen point of order %d is:" % l)
    #this point is across to elliptic curve
    P = findPoint2(C,l,p)
    print(P)
    print("Check if the order is correct:")
    print(l*P)


    ID = input("Enter the ID you want to use: ")
    #print("The ID is:")
    #ID = "steve@uni.lu"
    print(ID)

    #s in F_l^x
    print("s is equal to :")
    s = int(13)
    print(s)
    Ppub = s*P

    print("Ppub is equal to %s " % Ppub)

    print("-------------------------------")
    print("The hashed point is:")

    QID = hash(ID,C,p,P,l)
    print(QID)

    DID = s*QID
    print("DID is equal to: %s" % DID)
    outputFile.write('DID is equal to: '+str(DID)+'\n')

    print("-------------------------------")
    print("Alice part:")
    QIDAlice = hash(ID,C,p, P, l)

    print(QIDAlice)
    #r in F_l^x
    r = int(7)
    print("r is equal to:")
    print(r)


    print("-------------------------------")
    print("Test if points are of order")
    print(l)
    print("Point l*QID Alice")
    print(l*QIDAlice)
    print("Point l*Ppub")
    print(l*Ppub)

    print("-------------------------------")
    print("Weil pairing and verification")

    #define the points of the Elliptic Curve to the new
    #elliptic curve. we have an inclusion  
    #E(Fp) C E(Fp^2)
    #but for further computation, we need to be able to
    #work over the new elliptic curve (for the weil pairing)
    E2 = EllipticCurve2( Fp2([0]), Fp2([1]), Fp2)
    QIDAlice2 = Point2(E2, Fp2([QIDAlice.x.n]), Fp2([QIDAlice.y.n]))
    Ppub2 = Point2(E2, Fp2([Ppub.x.n]), Fp2([Ppub.y.n]))

    gID = ModifWeil(QIDAlice2, Ppub2, l , b)

    print("gID is equal to:")
    print(gID)

    print("Check if it is a lth rooth:")
    print(gID**(l)) 


    print("-------------------------------")
    print("Encryption")

    print("\n")
    M = input("Enter the message you want to encrypt: ")

    #M = "  hello, this is a test. are you sure this is working? I could easily break your decryption!"
    lengthMessage = len(M)

    print("The message to encrypt is : %s" % M)

    #decode the message to bytes and hash it
    b1 = bytearray(M.encode('utf-8'))
    hash = hash3(gID**(r), lengthMessage)

    #bitwise addition
    xor1 = xor(b1,hash)

    #create the cyphertext to send it to someone else
    cypher = Ciphertext(r*P,xor1)

    outputFile.write('First value of the cyphertext: '+str(cypher.a)+'\n')
    outputFile.write('Second value of the cyphertext: '+str(cypher.b)+'\n')

    print("The message after encryption in bytes: ")
    print(xor1)

    #create a hex representation of the encrypted message. this way, it is easier to communicate to a third party
    #and independent of the machine which is running.
    decoded = binascii.hexlify(xor1)

    outputFile.write("This is a hex representation of the encrypted message. This hex-code needs to be entered to the decryption script: " + str(decoded)[2:len(str(decoded))-1])

    #close file
    outputFile.close()
