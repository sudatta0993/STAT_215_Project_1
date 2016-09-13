# File: test_chisq.py

from ChiSq import manual_chi_sq
import py.test

def test_chisq_func():
	f_test_obs = list(i**2 for i in range(10))
	assert manual_chi_sq(f_test_obs) == 253