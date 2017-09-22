# Author: Jorge Hevia Moreno
# Contac: jmhev@outlook.com
# File: this file provides the functions needed to import
#		data from a csv file and use it

# library so we can read a csv 
# Installation: sudo pip install pandas
import pandas as pd
# module to read arguments
import sys
# check if the input is right
if len(sys.argv) < 2:
	print("Error: the program has less than 1 argument.")
	print("Usage: python adaline.py <file>")
	sys.exit(2)
if ".csv" is not str(sys.argv[1]):
	print("Error: that's not a csv file.")
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