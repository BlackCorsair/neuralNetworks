# Author: Jorge Hevia Moreno
# Contac: jmhev@outlook.com
# File: this file provides the functions needed to import
#		data from a csv file and use it

# library so we can read a csv 
# Installation: sudo pip install pandas
import pandas as pd
# module to read arguments
import sys
# mathematical module so we can use random numbers
import numpy as np
# check if the input is right
if len(sys.argv) < 2:
	print("Error: the program has less than 1 argument.")
	print("Usage: python adaline.py <file>")
	sys.exit(2)

if ".csv" not in str(sys.argv[1]):
	print("Error: that's not a csv file.")
	print("File entered: "+ str(sys.argv[1]))
	sys.exit(2)
print("File: " + str(sys.argv[1]))
# Read the CSV into a panda's data frame (df)
dataFrame = pd.read_csv(str(sys.argv[1]), delimiter=',')

# Export it as a list of tuples
data = [tuple(x) for x in dataFrame.values]


# ADALINE MODUS OPERANDI
'''
 1) Initialize random weights and threshold
 2) Show an initial input patron
 3) Calculate the output, compare it with the desired output and get the difference
 4) Re-calculate all the weights and threshold
 5) Modify the weights and threshold
 6) Repeat 2-5 for 1 cycle
 7) Repeat 2-6 until input criteria is met
'''

'''
	Name: initializerWT
	Function: it initializes the weights and threshold given
	Input: weights tuple and threshold value
	Returns: weights tuple and threshold value (in that order)
	TO-DO: use a heavier random generator
'''
def initializeWT(weights, threshold):
	for x in xrange(0, len(weights)):
		weights[x] = np.random.uniform(low=0.1, high=(1))
		print("Weight "+str(x) + " with initial random value: " +str(weights[x]))
	threshold = np.random.uniform(low=-1, high=(1))
	print("Threshold initial random value is: "+str(threshold))
	return weights, threshold

w = [0.0, 0.0, 0.0, 0.0, 0.0]
threshold = 0.0

w, threshold = initializeWT(w, threshold)
