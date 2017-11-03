# Author: Jorge Hevia Moreno
# Contac: jmhev@outlook.com
# File: this file provides the functions needed to import
#		data from a csv file and use it

# library so we can read a csv 
# Installation: sudo pip install pandas
import pandas as pd
import numpy as np
# Read the CSV into a panda's data frame (df)
dataFrame = pd.read_csv('../RandomizedData.csv', delimiter=',')

# Export it as a list of tuples
tuples = [list(x) for x in dataFrame.values]

print("Show a column")
print(dataFrame.rows)
print(x1)

print("Show a column")
for x in range(0, len(tuples)):
	print(dataFrame.values[x][0])
