import numpy as np

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
	cdef float error = 0.0
	cdef float output = 0.0
	for x in rows:
		# cdef float output = 0.0
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
	cdef float weightsTemp = 0.0
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
	for x in xrange(0, nCycles):
		weights, threshold = training(rows, weights, threshold, learnfactor)
		errorCalculatedTraining.append(calculateError(rows, weights, threshold))
		errorCalculatedValidated.append(calculateError(rows_validation, weights, threshold))		
	return weights, threshold, errorCalculatedTraining, errorCalculatedValidated