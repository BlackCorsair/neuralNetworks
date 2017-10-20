# Author: Jorge Hevia Moreno
# Co-Author: Luis Victor Hevia
# Contact: jmhev@outlook.com
# File: this file provides the functions needed to import
#		data from a csv file and use it


################################################################################################################
################################################################################################################
# ERROR TREATMENT AND INITIAL READS
################################################################################################################
################################################################################################################

'''
	Name: colors
	Function: contains a set of strings to change the terminal color
'''
class colors:
	WARNING = "\033[93m"
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	FAIL = "\033[91m"
	ENDC = "\033[0m"

# library so we can read a csv 
# Installation: sudo pip install pandas
import pandas as pd
# module to read arguments
import sys
# mathematical module so we can use random numbers
import numpy as np
# check if the input is right
if len(sys.argv) < 6:
	print(colors.FAIL + "Error: the program has less than 6 arguments." + colors.ENDC)
	print(colors.WARNING  + "Usage: python adaline.py <training-file> <validation-file> <test-file> <number of inputs/weights> <number of cycles>" + colors.ENDC)
	sys.exit(2)
if len(sys.argv) > 6:
	print(colors.FAIL + "Error: the program has more than 6 arguments." + colors.ENDC)
	print(colors.WARNING  + "Usage: python adaline.py <training-file> <validation-file> <test-file> <number of inputs/weights> <number of cycles>" + colors.ENDC)
	sys.exit(2)
for x in xrange(2,4):
	if ".csv" not in str(sys.argv[x]):
		print(colors.FAIL  + "Error: that's not a csv file.")
		print(colors.WARNING  + "File entered: "+ str(sys.argv[x])  + colors.ENDC)
		sys.exit(2)
''' old error reporting
if ".csv" not in str(sys.argv[1]) and :
	print(colors.FAIL  + "Error: that's not a csv file.")
	print(colors.WARNING  + "File entered: "+ str(sys.argv[1])  + colors.ENDC)
	sys.exit(2)
end of old error reporting
'''
print(colors.OKBLUE+"File: " + str(sys.argv[1])+colors.ENDC)
# Read the CSV into a panda's data frame (df)
dataFrameTraining = pd.read_csv(str(sys.argv[1]), delimiter=',')
dataFrameValidation = pd.read_csv(str(sys.argv[2]), delimiter=',')
dataFrameTests = pd.read_csv(str(sys.argv[3]), delimiter=',')

# Export it as a list of tuples
dataTraining = [np.matrix(x) for x in dataFrameTraining.values]
dataValidation = [np.matrix(x) for x in dataFrameValidation.values]
dataTests = [np.matrix(x) for x in dataFrameTests.values]

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
	error = error * 1/len(rows)
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
'''
	Name: training
	Function: makes one cylce of training (from 3 to 5)
	Input: rows, weights, threshold, learnfactor 
	Returns: weights, threshold after the training
'''
def training(rows, weights, threshold, learnfactor):
	for x in rows:
		output = calculateOutputPerRow(x[0:8], weights, threshold)
		weights, threshold = modifyWeights(output, x, weights, threshold, learnfactor)
	return weights, threshold
'''
	Name: cycle
	Function: executes 'n' times training, calcerror, validation (which is
			calcerror with validation rows), calcerror
	Input: rows, weights, threshold, learnfactor, rows_validation, nCycles
	Returns: weights, threshold after the training
'''
def Cycle(rows, rows_validation, weights, threshold, learnfactor, nCycles):
	errorCalculatedTraining = []
	errorCalculatedValidated = []
	for x in nCycles:
		weights, threshold = training(rows, weights, threshold, learnfactor)
		errorCalculatedTraining.append(calculateError(rows, weights, threshold))
		errorCalculatedValidated.append(calculateError(rows_validation, weights, threshold))		
	return weights, threshold, errorCalculatedTraining, errorCalculatedValidated
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
for x in xrange(0, int(sys.argv[4])):
	weights.append(0.0)
# Initialize weights and thresholds with random float numbers between -1 and 1
weights, threshold = initializeWT(weights, threshold)
rows = getRows(dataFrameTraining)
rows_validation = getRows(dataFrameValidation)
rows_tests = getRows(dataFrameTests)
# calculates error
#accumulatedError = calculateError(rows, weights, threshold)
#print(accumulatedError)
'''
print("\n")
weights, threshold = training(rows, weights, threshold, learnfactor)
print(colors.OKGREEN+"first weights calc: " + colors.OKBLUE+ str(weights) + ", threshold: " + str(threshold)+ colors.ENDC)
weights, threshold = training(rows, weights, threshold, learnfactor)
print(colors.OKGREEN+"weights after training: "+ colors.OKBLUE+ str(weights) + ", threshold: " + str(threshold)+ colors.ENDC)
'''
errorTraining = []
errorValidated = []
print(colors.WARNING + "TESTING CYCLE" + colors.ENDC)
weights, threshold, errorTraining, errorValidated = Cycle(rows, rows_validation, weights, threshold, learnfactor, sys.argv[5])
print(colors.OKBLUE + "TESTING CYCLE FINISHED" + colors.ENDC)
print(colors.OKGREEN+"weights calculated: " + colors.OKBLUE+ str(weights) + colors.OKGREEN + "\nthreshold: " + colors.OKBLUE+ str(threshold)+ colors.ENDC)
