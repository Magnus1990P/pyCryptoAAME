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
##	Imports
#######################################################
import sys

#######################################################
##	Variables 
#######################################################
binary	= []		#Binary holder for b, the reverse binary sequence of b
modExp	= []		#Modulated calculations, holds the output val of mod exp calcs
base		= []		#Base value holder, n-1 length array

a 			= 0			#Integer base value
b				= 0			#Integer exponential value
n 			= 0			#Integer modulus value
ML			= 5			#Max integer length for printing scientific numbers
K				= 2			#Fixed value to use as exponential value and divisor

#######################################################
##	Input parameter check
#######################################################
if len( sys.argv ) != 4:
	print "Execute program with the following command:\n\t" 		\
				"./main.py [base (a)] [exponent (b)] [mod (n)]\n" 		\
				"Eg. './main 2 1234 789', should output 481 as "			\
				"shown on p78-79 in Trappe and Washinton 2nd Ed\n"		
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
##	Helper function to print headings
#######################################################
def title( d, n, out ):
	print "\n%s\n%s\t%s\n%s" % (d*n, d, out, d*n)	#Print divisor, string, divisor

#######################################################
##	Helper function to print large numbers
#######################################################
def sciNum( c ):
	if c < 10000:
		return str( c )

	s = str( c )										#Convert number to string
	t = len(s)-1										#number of e
	l = list(s[:ML])								#Convert 5 first numbers to list
	l.insert(1, ".")								#Add a comma after first number

	o = ""
	if t > 0:												#If org number is more than 10
		o = "".join(l) + "e+%d"  % t	#Create scientific number
	else:																				
		o = "".join(l) + "0e+%d" % t	#Add after comma when appending

	return o

#######################################################
##	Returns a list of "num"s bin val in rev order
#######################################################
def getBinary( num, bi ):					
	if num == 0 or num == 1:				#If last run value is 0 / 1
		bi.append( num )							#Append the value to binary representation
		print "%35s  ->%7s  |   mod(%d)  = %5d" % ( str(num), str(num), K, num ) 	
		return bi											#Return the finished binary sequence

	x = num % K											#Grab the remainder, just using modulo operand
	bi.append( x )									#Append binary value to list
																	#Print the calculation
	print "%13d / %2d %8s %7s  -> %6s  |   mod(%d)  = %5d" % ( num, K, "=", 
			str(num/a), str(num), K, x ) 	

	bi = getBinary( (num/K), bi )		#Recursive call to create the bin sequence
	return bi


#######################################################
##	Calculates all base numbers for use in modExp 
#######################################################
def calcBase( I ):
	global base
	if I >= len(binary):													#Cutoff function to finish calc
		return																			#return to escape function
	elif I == 0:																	#First calculation
		base.append( (a**K) % n)										#append a^2 mod(n) as first val
		print "%10d^%4d | mod(%d) == %12d^%d | mod(%d) == %10s | mod(%d) == %d" % \
		(K, (K**I), n, a, K, n, sciNum(base[I]), n, base[I] ) 
	else:																					#If not finished
		base.append( (base[I-1] ** K) % n )					#Add congruence value
		print "%10d^%4d | mod(%d) == %12d^%d | mod(%d) == %10s | mod(%d) == %d" % \
		(K, (K**I), n, base[I-1], K, n, sciNum(base[I-1]**K), n, base[I] ) 
	calcBase( I+1 )


#######################################################
##	Recursive function to calculate the mod exp
#######################################################
def calcModExp( I ):
	global modExp 																#Global values to use
	if I >= len(binary):													#Cutoff function to finish calc
		return																			#return to escape function
	elif I == 0:																	#If first calculation
		if binary[I] == 1:													#If calculation should be made
			modExp.append( (1 * a ) % n)							#Static calculation
			print "%d -> %6d^%4d | mod(%d) = %7d * " \
						"%4d | mod(%d) == %d" % (binary[I], 
								a, b, n, 1, a, n,	modExp[0])		#print first calc line
		if binary[I] == 0:													#If calculation should be made
			modExp.append( 1 )							#Static calculation
			print "%d -> %22s = %25s == %d" % (binary[I], " ", " "	,	modExp[I])

	else:																					#If not finished
		d = modExp[I-1]															#Prev modExp
		e = base[I-1]																#Prev base value
		
		if binary[I] == 1:													#If calculation should be made
			f = (d * e)																#new modExp value
			g = f % n																	#new modExp value	
			modExp.append( g )												#Add modExp value to list

			print "%d -> %22s = %7d * %4d | mod(%d) == %d" %(binary[I], " ", d,e,n,g)
		else:																				#Print intermediate line
			print "%d -> %22s = %25s == %d" % (binary[I], " ", " "	,	modExp[I-1])
			modExp.append( modExp[I-1] )							#Add previous modExp value

	calcModExp( I+1 )															#Recursive call to nex calc



#######################################################
##	Main running function
#######################################################
title( "#", 80, "Converting %d from base 10 to base %d" % (b,K))
binary = getBinary( b, [] )						#calculate the reverse binary sequence
																			#Print bin seq in correct order high->low
print "\tInt %d converted to %d base: " % ( b, K),
for x in binary[::-1]:								
	print x,
print 

title("#",80, "Calculating base numConverting %d from base 10 to base %d"%(b,K))
calcBase( 0 )

title( "#", 80, "Calculating the modular exponentiations")
calcModExp( 0 )								#Start to calculate the mod exponentials


title( "#",80, "%d^%d | mod(%d) = %d" % (a, b, n, modExp[len(modExp)-1] ) )


