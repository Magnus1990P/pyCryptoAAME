#!/usr/bin/env python
########################################################
#	Stud nr:	090832
#	Date:			05.09.2015
#
# Project:	RSA
#	Program:	Arrow Algorithm and Modular exponentiation
#	Descr:		Implementation of the arrow algorithm 
#						with the use of modular exponentiation
########################################################
#######################################################
##
#######################################################

#######################################################
##	Imports
#######################################################
import sys

#######################################################
##	Variables 
#######################################################
binary	= []		#Binary holder for b, the reverse binary sequence of b
modExp	= []		#Modulated calculations, holds the output val of mod exp calcs
congr		= []		#Congruence value holder, n-1 length array

a 	= 0						#Integer base value
b		= 0						#Integer exponential value
n 	= 0						#Integer modulus value
ML	= 5						#Max integer length for printing
#######################################################
##	Input parameter check
#######################################################
if len( sys.argv ) != 4:
	print "Execute program with the following command:\n\t" 		\
				"./main.py [base (a)] [exponent (b)] [mod (n)]\n" 		\
				"Eg. './main 2 1234 789', should output 481 as "			\
				"shown on p78-79 in Trappe and Washinton 2nd Ed\n"		\
				"NB! This program works only on positive integers.\n" 
	exit()

try:													#Try to convert input arg to integer values
	a = int( sys.argv[1] )			#Grab base number of expresison from argument list
	b = int( sys.argv[2] )			#Grab the exponential value from argument list
	n = int( sys.argv[3] )			#Grab the modulus value from argument list
except:												#If conversion to integer failse print error
	print "Incorrect input, try again ['%s', '%s', '%s']" % (sys.argv[1],
			sys.argv[2], sys.argv[3])
	exit()


#######################################################
##	Returns a list of "num"s bin val in rev order
#######################################################
def getBinary( num, bi ):					
	if num == 0 or num == 1:				#If last run value is 0 / 1
		bi.append( num )							#Append the value to binary representation
		print "%35s  ->%7s  |   mod(%d)  = %5d" % ( str(num), str(num), a, num ) 	
		return bi											#Return the finished binary sequence

	x = num % a											#Grab the remainder, just using modulo operand
	bi.append( x )									#Append binary value to list
																	#Print the calculation
	print "%13d / %2d %8s %7s  -> %6s  |   mod(%d)  = %5d" % ( num, a, "=", 
			str(num/a), str(num), a, x ) 	

	bi = getBinary( (num/a), bi )		#Recursive call to create the bin sequence
	return bi

#######################################################
##	Helper function to print headings
#######################################################
def title( d, n, out ):
	print "\n%s\n%s\t%s\n%s" % (d*n, d, out, d*n)	#Print divisor, string, divisor

#######################################################
##	Recursive function to calculate the mod exp
#######################################################
def calcModExp( B, I ):
	global modExp, congr, a, b, n									#Global values to use
	if I >= len(B):																#Cutoff function to finish calc
		return																			#return to escape function
	else:																					#If not finished
		if I < len(B)-1:														#Avoid creating last congruence
			congr.append( congr[I-1] ** a )						#Add congruence value
		x = congr[I-1]**a														#Calc simpler exponential val
		y = x % n																		#The modulus
		modExp.append( y )													#Append the modExp value to list

		w1	= "(" + str(a) + "^" + str(a**I) + ")"	#Generate output string part 1

		s = str(congr[I-1])													#Create scientific number
		l = list(s[:ML])
		l.insert(1, ".")
		if len(s)-1 > 0:
			o = "".join(l) + "e+%d" % int(len(s)-1)
		else:
			o = "".join(l) + "0e+%d" % int(len(s)-1)

																								#Generate output string part 2
		w2	= "(%13s ^ %d )" % (o, a)
																								#Create the output string
		out = "%12s | mod(%d) == %17s | mod(%d) == %5s" % (w1, n, w2, n, y)
		print out																		#Print calculation
		calcModExp( B, I+1 )												#Recursive call to nex calc




#######################################################
##	Main running function
#######################################################
title( "#", 80, "Converting %d from base 10 to base %d" % (b,a))
binary = getBinary( b, [] )						#calculate the reverse binary sequence

																			#Print bin seq in correct order high->low
print "\tInt %d converted to %d base: " % ( b, a),
for x in binary[::-1]:
	print x,

modExp.append( binary[0] )						#Add initial modExponential value
congr.append( a )											#append base value as first congruence val

title( "#", 80, "Calculating the modular exponentiations")
calcModExp( binary, 1 )								#Start to calculate the mod exponentials

title( "#", 80, "Calculating the final modular exponential value.")
s = "%d^%d | mod(%d)" % (a,b, n)

calc = ""
ans = 1
L = len(binary)-1
if b >= 1:
	for i in range( 0, len(binary) ):
		if binary[L-i] == 1:
			if ans > 1:
				calc = calc + " * "
			calc = calc + "%d" % modExp[L-i]
			ans = ( ans * modExp[L-i] )
		modExp[i]

print "%22s = %s | mod( %d )" % (s, calc, n)
print "%22s = %d | mod( %d )" % (" ", ans, n)
print "%22s = %5d" %(" ", (ans%n) )
print " "*25 + "="*6


