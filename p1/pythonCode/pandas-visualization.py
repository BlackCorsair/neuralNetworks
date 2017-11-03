# this file has the only purpose to serve as an example of the power of 
# pandas for data visualization
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib

matplotlib.style.use('ggplot')

# df = pd.DataFrame(np.random.randn(10,4), index = pd.date_range('1/1/2000'), periods = 10, columns = list('ABCD'))
df = pd.read_csv('../RandomizedData.csv', delimiter=',')
df.cumsum()
df.plot()


plt.show()