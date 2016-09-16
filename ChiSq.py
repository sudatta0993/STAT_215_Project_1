# File: ChiSq.py

import sys
import numpy as np
import scipy
import scipy.stats
import pandas as pd
from summary_stat import load_dataset

# Define function to take only terminal digits of data
def terminal_digit(num):
	return int(num % 10)

# Define function to shape data from authors into a vector
def clean_data(data):
	del data['average'] # Keep only count columns; discard average
	vec_data = data.stack()

	return vec_data

# Calculate observed frequency of each terminal digit
def term_digit_freq(vect):
	end_digit = vect.apply(terminal_digit)
	f_obs = np.bincount(end_digit)
	
	return f_obs

# Define function that "manually" computes chi squared test statistic
def manual_chi_sq(f_obs):
	n = sum(f_obs) # Total sample size
	p = 0.1 # Hypothesized proportion of each level
	E = n*p # Expected frequency count per level (equal for all levels)

	chi2 = 0
	for x in f_obs: 
		chi2 = chi2 + ((x - E)**2)/E
	return chi2

def run(filelocation, skiprows, usecols):
	(data, total, complete) = load_dataset(filelocation, skiprows, usecols)
	vec_data = clean_data(data)
	f_obs = term_digit_freq(vec_data)
	
	# Calculate chi sq statistic via two methods + p-value using Python function
	manual_chi2 = manual_chi_sq(f_obs)
	chi2, p = scipy.stats.chisquare(f_obs) 
	return (manual_chi2, chi2, p, f_obs)

if __name__ == "__main__":
	print ("RTS colony (Manual Chi Sq, Chi Sq, p-value, f_obs) = ", run('./data/OSF_Storage/Bishayee Colony Counts 10.27.97-3.8.01.csv', 2, ["col1","col2","col3","average"]))
	# print ("RTS coulter (Manual Chi Sq, Chi Sq, p-value, f_obs) = ", run('./data/OSF_Storage/Bishayee Coulter Counts.10.20.97-7.16.01.csv', 1, ["Count 1", "Count 2", "Count 3", "Average"]))
	# print ("Others colony (Manual Chi Sq, Chi Sq, p-value, f_obs) = ", run('./data/OSF_Storage/Other Investigators in Lab.Colony Counts.4.23.92-11.27.02.csv',1,["col1","col2","col3","average"]))
	# print ("Others coulter (Manual Chi Sq, Chi Sq, p-value, f_obs) = ", run('./data/OSF_Storage/Other Investigators in Lab.Coulter Counts.4.15.92-5.21.05.csv',1,["Coul 1","Coul 2","Coul 3","Average"]))
	# print ("Outside lab 1 coulter (Manual Chi Sq, Chi Sq, p-value, f_obs) = ", run('./data/OSF_Storage/Outside Lab 1.Coulter Counts.6.7.91-4.9.99.csv',0,[1,2,3,4]))
	# print ("Outside lab 2 coulter (Manual Chi Sq, Chi Sq, p-value, f_obs) = ", run('./data/OSF_Storage/Outside Lab 2.Coulter Counts.6.6.08-7.7.08.csv',1,["Count 1", "Count 2", "Count 3", "Average"]))
	# print ("Outside lab 3 colony (Manual Chi Sq, Chi Sq, p-value, f_obs) = ", run('./data/OSF_Storage/Outside Lab 3.Colony Counts.2.4.10-5.21.12.csv',1,["c1", "c2", "c3", "average"]))