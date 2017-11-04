import adaline as ad	
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

matplotlib.style.use('ggplot')
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
# HERE'S WHERE THE MAGIC HAPPENS
################################################################################################################
################################################################################################################

# learn factor
learnfactor = 0.0001
# first we create a lists of weights, outputs and desiredOutputs, then the treshold variable
weights = []
output = [] # output list with calculated values
desiredOutput = [] # desired output list
threshold = 0.0
# and then initialize the weights list with the number of inputs
for x in xrange(0, int(sys.argv[4])):
	weights.append(0.0)
# Initialize weights and thresholds with random float numbers between -1 and 1
weights, threshold = ad.initializeWT(weights, threshold)
rows = ad.getRows(dataFrameTraining)
rows_validation = ad.getRows(dataFrameValidation)
rows_tests = ad.getRows(dataFrameTests)
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
weights, threshold, errorTraining, errorValidated = ad.Cycle(rows, rows_validation, weights, threshold, learnfactor, int(sys.argv[5]))
print(colors.OKBLUE + "TESTING CYCLE FINISHED" + colors.ENDC)


# printing
baseOutput = []
baseOutputVal = []

#plt.xlim([0,1000])
plt.plot(errorTraining, 'b', errorValidated, 'r')
#plt.show()
#pls.close()