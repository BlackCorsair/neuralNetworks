	# Author: Jorge Hevia Moreno
# Contact: jmhev@outlook.com
# File: this file provides the functions needed to import
#		data from a csv file and use it


################################################################################################################
################################################################################################################
# ERROR TREATMENT AND INITIAL READS
################################################################################################################
################################################################################################################



# library so we can read a csv 
# Installation: sudo pip install pandas
import pandas as pd
# module to read arguments
import sys
# mathematical module so we can use random numbers
import numpy as np
# check if the input is right
if len(sys.argv) < 3:
	print("Error: the program has less than 2 arguments.")
	print("Usage: python adaline.py <file> <number of inputs/weights>")
	sys.exit(2)

if ".csv" not in str(sys.argv[1]):
	print("Error: that's not a csv file.")
	print("File entered: "+ str(sys.argv[1]))
	sys.exit(2)
print("File: " + str(sys.argv[1]))
# Read the CSV into a panda's data frame (df)
dataFrame = pd.read_csv(str(sys.argv[1]), delimiter=',')

# Export it as a list of tuples
data = [np.matrix(x) for x in dataFrame.values]

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

################################################################################################################
################################################################################################################
# FUNCTION DEFINITIONS
################################################################################################################
################################################################################################################


'''
	Name: initializerWT
	Function: it initializes with random values between -1.0 and 1.0 the weights and threshold given
	Input: weights list and threshold value
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
def getRows(data):
	# create a list of numpy arrays
	# every np.array will contain a row
	rows = []
	for x in data.values:
		rows.append(np.array(x))
	return rows
	#end

'''
	Name: calculateOutputPerRow
	Function: it calculates the output given the inputs from the 
				csv file and some random weights
	Input: row array, weights and threshold
	Returns: the outputs (y) np.array
'''
def calculateOutputPerRow(row, weights, threshold):
	return row.dot(np.array(weights)) + threshold

'''
	Name: calculateError
	Function: it calculates the total error given the inputs from the 
				csv file and some random weights
	Input: rows list, weights and threshold
	Returns: the outputs (y) np.array
'''
def calculateError(rows, weights, threshold):
	error = 0.0
	for x in rows:
		output = calculateOutputPerRow(x[0:8], weights, threshold)
		error = error + (x[8] - output)**2 # test this line
	error = error * 1/2 * 1/len(rows)
	return error
'''
	Name: modifyWeights
	Function: modifies the weights and threshold given the output
				calculated from the row (also given)
	Input: output calculated from row, row, weights vector, threhold, learnfactor
	Returns: modified weights vector and threshold
'''
def modifyWeights(output, row, weights,  threshold, learnfactor):
	weightsTemp = 0.0
	learnedDiff = learnfactor * (row[8] - output)
	for x in xrange(0, len(weights)):
		weightsTemp = learnedDiff * row[x] # learnedDiff is calculated outside the loop for better performance
		weights[x] = weights[x] + weightsTemp
	threshold = threshold + learnedDiff
	return weights, threshold
################################################################################################################
################################################################################################################
# HERE'S WHERE THE MAGIC HAPPENS
################################################################################################################
################################################################################################################

# learn factor
learnfactor = 0.1
# first we create a lists of weights, outputs and desiredOutputs, then the treshold variable
weights = []
output = [] # output list with calculated values
desiredOutput = [] # desired output list
threshold = 0.0
# and then initialize the weights list with the number of inputs
for x in xrange(0, int(sys.argv[2])):
	weights.append(0.0)

inputs = []

# Initialize weights and thresholds with random float numbers between -1 and 1
weights, threshold = initializeWT(weights, threshold)
rows = getRows(dataFrame)
# calculates error
accumulatedError = calculateError(rows, weights, threshold)
print(accumulatedError)

output = calculateOutputPerRow(rows[0][0:8], weights, threshold)
weights, threshold = modifyWeights(output, rows[0], weights, threshold, learnfactor)
print("first weights calc: "+ str(weights))

output = calculateOutputPerRow(rows[0][0:8], weights, threshold)
weights, threshold = modifyWeights(output, rows[0], weights, threshold, learnfactor)
print("second weights calc: "+ str(weights))