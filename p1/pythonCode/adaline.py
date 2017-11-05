	# Author: Jorge Hevia Moreno
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

# libraries to visualize dataTraining
import matplotlib.pyplot as plt
import matplotlib
import csv
matplotlib.style.use('ggplot')
# library so we can read a csv 
# Installation: sudo pip install pandas matplotlib numpy
import pandas as pd
# module to read arguments
import sys
# mathematical module so we can use random numbers
import numpy as np
# check if the input is right
if len(sys.argv) < 7:
	print(colors.FAIL + "Error: the program has less than 6 arguments." + colors.ENDC)
	print(colors.WARNING  + "Usage: python adaline.py <training-file> <validation-file> <test-file> <number of inputs/weights> <number of cycles> <learnfactor>" + colors.ENDC)
	sys.exit(2)
if len(sys.argv) > 7:
	print(colors.FAIL + "Error: the program has more than 6 arguments." + colors.ENDC)
	print(colors.WARNING  + "Usage: python adaline.py <training-file> <validation-file> <test-file> <number of inputs/weights> <number of cycles> <learnfactor>" + colors.ENDC)
	sys.exit(2)
for x in xrange(2,4):
	if ".csv" not in str(sys.argv[x]):
		print(colors.FAIL  + "Error: that's not a csv file.")
		print(colors.WARNING  + "File entered: "+ str(sys.argv[x])  + colors.ENDC)
		sys.exit(2)

print(colors.OKBLUE+"Reading files: " + str(sys.argv[1]) + str(sys.argv[2]) + str(sys.argv[3]) + "..." +colors.ENDC)
# Read the CSV into a panda's data frame (df)
dataFrameTraining = pd.read_csv(str(sys.argv[1]), delimiter=',')
dataFrameValidation = pd.read_csv(str(sys.argv[2]), delimiter=',')
dataFrameTests = pd.read_csv(str(sys.argv[3]), delimiter=',')

print(colors.OKBLUE+"Exporting files into readable values..." +colors.ENDC)
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
	threshold = np.random.uniform(low=-1, high=(1))
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
		output = calculateOutputPerRow(x[0:len(weights)], weights, threshold)
		error = error + (x[len(weights)] - output)**2 # test this line
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
	learnedDiff = learnfactor * (row[len(weights)] - output)
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
		output = calculateOutputPerRow(x[0:len(weights)], weights, threshold)
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
	for x in xrange(0, nCycles):
		weights, threshold = training(rows, weights, threshold, learnfactor)
		errorCalculatedTraining.append(calculateError(rows, weights, threshold))
		errorCalculatedValidated.append(calculateError(rows_validation, weights, threshold))		
	return weights, threshold, errorCalculatedTraining, errorCalculatedValidated
'''
	Name: Predict
	Function: calculates the output from the testing rows and then saves it in an array
	Input: row, weights, threshold
	Returns: an array of outputs
'''
def Predict(rows, weights, threshold):
	predictedOutput = []
	for row in rows:
		predictedOutput.append(calculateOutputPerRow(row[0:len(weights)], weights, threshold))
	return predictedOutput

################################################################################################################
################################################################################################################
# HERE'S WHERE THE MAGIC HAPPENS
################################################################################################################
################################################################################################################
print(colors.OKBLUE+"Initializing values..." +colors.ENDC)
# learn factor
learnfactor = float(sys.argv[6])
# first we create a lists of weights, outputs and desiredOutputs, then the treshold variable
weights = []
output = [] # output list with calculated values
desiredOutput = [] # desired output list
threshold = 0.0
# and then initialize the weights list with the number of inputs
for x in xrange(0, int(sys.argv[4])):
	weights.append(0.0)

print(colors.OKBLUE+"Generating values to analyze..." +colors.ENDC)
# Initialize weights and thresholds with random float numbers between -1 and 1
weights, threshold = initializeWT(weights, threshold)
rows = getRows(dataFrameTraining)
rows_validation = getRows(dataFrameValidation)
rows_tests = np.array(dataFrameTests)

print(colors.OKBLUE+"Training..." +colors.ENDC)

errorTraining = []
errorValidated = []
weights, threshold, errorTraining, errorValidated = Cycle(rows, rows_validation, weights, threshold, learnfactor, int(sys.argv[5]))
print(colors.OKBLUE + "TESTING CYCLE FINISHED" + colors.ENDC)
print(colors.OKBLUE+"Training done." +colors.ENDC)

print(colors.OKBLUE+"Forecasting testing output..." +colors.ENDC)
predictedOutput = Predict(rows_tests, weights, threshold)
print(colors.OKBLUE+"Predicted output saved." +colors.ENDC)

# printing
baseOutput = []
baseOutputVal = []

plt.xlabel('Iterations from 0 to '+ sys.argv[5])
plt.ylabel('Error across the Iterations')
plt.plot(errorTraining, c='b', label="Training error")
plt.plot(errorValidated, c='r', label="Validation error")
plt.legend()

# WRITING FILES
outputsTxt = 'outputs-nIterations-'+sys.argv[5]+'-learnfactor-'+str(learnfactor)+'.csv'
weightsTxt = 'weights-nIterations-'+sys.argv[5]+'-learnfactor-'+str(learnfactor)+'.csv'
weights.append(threshold)
plot = 'plot-nIterations-'+sys.argv[5]+'-learnfactor-'+str(learnfactor)+'.png'
np.savetxt(outputsTxt, np.array(predictedOutput), delimiter=",")
np.savetxt(weightsTxt, np.array(weights), delimiter=",")
plt.savefig(plot, dpi=500)
print(colors.OKGREEN +"Writing files:\n- "+outputsTxt+"\n- "+weightsTxt+"\n- "+plot + colors.ENDC)