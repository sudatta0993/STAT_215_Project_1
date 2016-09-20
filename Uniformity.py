# File: Uniformity.py

import sys
import numpy as np
import scipy
import scipy.stats
import pandas as pd
import matplotlib.pyplot as plt
from summary_stat import load_dataset
from ChiSq import terminal_digit
from ChiSq import term_digit_freq

# Define function to test uniformity assumption
def uniformity(data):
	means = data['average'] # Use means as lambda values, as per author assumptions
	s = np.random.poisson(lam = (means), size = (3,len(means))) # Generate random sets of triples
	ran_poi_vect = pd.Series(np.reshape(s,s.size))

	return ran_poi_vect

def run(filelocation, skiprows, usecols):
  (data, total, complete) = load_dataset(filelocation, skiprows, usecols)
  ran_poi_vect = uniformity(data)
  f_obs_test = term_digit_freq(ran_poi_vect)
  x = np.arange(10)
  
  # plot histogram
  plt.figure(figsize = (8,6))
  plt.hist(x, weights = f_obs_test, bins = np.arange(11), alpha = 0.5)
  plt.title("Test of Uniformity of Terminal Digit Distribution")
  plt.xlabel("Terminal Digit")
  plt.ylabel("Digit Counts")
  plt.grid(True)
  plt.show()
  
  chi2, p = scipy.stats.chisquare(f_obs_test)

  return (f_obs_test, chi2, p)

if __name__ == "__main__":
	print ("RTS colony (f_obs_test, chi2, p) = ", run('./data/OSF_Storage/Bishayee Colony Counts 10.27.97-3.8.01.csv', 2, ["col1","col2","col3","average"]))
	print ("RTS coulter (f_obs_test, chi2, p) = ", run('./data/OSF_Storage/Bishayee Coulter Counts.10.20.97-7.16.01.csv', 1, ["Count 1", "Count 2", "Count 3", "Average"]))
	print ("Others colony (f_obs_test, chi2, p) = ", run('./data/OSF_Storage/Other Investigators in Lab.Colony Counts.4.23.92-11.27.02.csv',1,["col1","col2","col3","average"]))
	print ("Others coulter (f_obs_test, chi2, p) = ", run('./data/OSF_Storage/Other Investigators in Lab.Coulter Counts.4.15.92-5.21.05.csv',1,["Coul 1","Coul 2","Coul 3","Average"]))
	print ("Outside lab 1 coulter (f_obs_test, chi2, p) = ", run('./data/OSF_Storage/Outside Lab 1.Coulter Counts.6.7.91-4.9.99.csv',0,[1,2,3,4]))
	print ("Outside lab 2 coulter (f_obs_test, chi2, p) = ", run('./data/OSF_Storage/Outside Lab 2.Coulter Counts.6.6.08-7.7.08.csv',1,["Count 1", "Count 2", "Count 3", "Average"]))
	print ("Outside lab 3 colony (f_obs_test, chi2, p) = ", run('./data/OSF_Storage/Outside Lab 3.Colony Counts.2.4.10-5.21.12.csv',1,["c1", "c2", "c3", "average"]))