# Author: Jorge Hevia Moreno
# Contac: jmhev@outlook.com
# File: this file provides the functions needed to import
#		data from a csv file and use it

# library so we can read a csv 
# Installation: sudo pip install pandas
import csv, sys
import numpy as np

columns = []
with open("../RandomizedDataTraining.csv", 'rb') as f:
	reader = csv.reader(f)
	try:
		for row in reader:
			column = np.array(row[i] for i in xrange(0, len(row)))
			print column
			columns.append(column)
	except csv.Error as e:
		sys.exit()
print(columns[0])