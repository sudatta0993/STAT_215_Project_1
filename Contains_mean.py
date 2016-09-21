import math
from scipy.stats import poisson
from scipy.stats import binom
from scipy.stats import norm
import numpy as np
import pandas as pd
from summary_stat import load_dataset
from summary_stat import mean_in_triplet

# Define a function to compute the probability when a triplet contains its mean for lambda, and the result will be stored
# in the vector probs.
def prob(probs):
    for i in range(2081):
        if i < 2001:
            lam = i
        else:
            lam = 100 * (i - 2000) + 2000
        n = poisson.ppf(1 - math.pow(10, -9), lam)
        n = n.astype(int)
        sum = 0
        tempar = np.array([0.0] * (n + 1)) # use an array to store the pmf of poisson(lambda)
        tempar[lam] = poisson.pmf(lam, lam) # start with the peak p(X = lambda)
        tempar[0] = poisson.pmf(0, lam)
        for i1 in range(lam - 1, 0, -1):
            tempar[i1] = tempar[i1 + 1] * (float(i1 + 1) / float(lam)) # Compute p(X = lambda') where lambda' < lambda
        for i2 in range(lam + 1, n + 1):
            tempar[i2] = tempar[i2 - 1] * (float(lam) / float(i2)) # Compute p(X = lambda') where lambda' < lambda
        for j in range(2, n + 1):
            odd = int(j % 2 == 1)
            for k in range(j, n + 1):
                sum += 6 * tempar[k - j] * (tempar[k - int(j / 2)] + odd * tempar[k - int(j / 2) - 1]) * tempar[k]
        probs[i] = sum
    return probs

# Compute the table of probability when lambda = 0, 1, 2, ..., 2000
probs_lambda = np.array([0.0] * 2081)
probs_lambda = prob(probs_lambda)


# Given a list of unequal probs for independent Bernoulli r.v., it'll return the cdf P(X <= x). This algorithm is based on the recursion scheme of coefficients of the
# moment generating function
def poibin(probs, x):
    n = len(probs)
    # Probs of complementary event for each Bernoulli trial
    q = 1 - probs
    # Induction of Coefficients
    a = np.zeros((n + 1,n + 1))
    for i in range(1, n + 1):
        for j in range(i + 1):
            if i == 1 and j == 0:
                a[i][j] = q[0]
            elif i == 1 and j == 1:
                a[i][j] = probs[0]
            elif i >= 2 and j == 0:
                a[i][j] = a[i - 1][j] * q[i - 1]
            elif j == i:
                a[i][j] = a[i - 1][j - 1] * probs[i - 1]
            else:
                a[i][j] = a[i - 1][j - 1] * probs[i - 1] + a[i - 1][j] * q[i - 1]
    pdf = a[n, :]
    cdf = np.cumsum(pdf)
    return cdf[x]

def run(file_location, skiprows, usecols, probs_lambda):
    (data, total, complete) = load_dataset(file_location, skiprows, usecols)
    data.columns = ['col1', 'col2', 'col3', 'average']
    # Rounded mean for each triplet
    mean = np.round(pd.np.array(data['average']).astype(np.double))
    # Throw the big lambda (when it is greater than 10000)
    mean = mean[(mean <= 10000)]
    # Initialize prob = 0 to each triplet
    probs = np.array([0.0] * len(mean))
    # Assign prob to each triplet
    for i in range(len(mean)):
        rounded_mean = int(mean[i])
        if rounded_mean <= 2000:
            index = rounded_mean
        else:
            rounded_mean = int(round(rounded_mean / 100.0) * 100)
            index = int(2000 + (rounded_mean - 2000) / 100)
        probs[i] = float(probs_lambda[index])
    # Compute # mean contained in triplet
    no_mean = mean_in_triplet(data, 'col1', 'col2', 'col3', 'average')
    # Actual p value
    p_value = 1 - poibin(probs, no_mean - 1)
    # Expected # mean contained in triplet
    no_expected = np.sum(probs)
    # Standard deviation
    Sd = math.sqrt(probs.dot(1 - probs))
    # Z-value
    z = (no_mean - no_expected) / Sd
    # Normal estimation of p_values
    p_value_for_normal = 1 - norm.cdf(z)
    return (p_value, no_mean, no_expected, Sd, z, p_value_for_normal)
# Compute the upper bound for p-value
def run_1(file_location, skiprows, usecols, probs_lambda):
    (data, total, complete) = load_dataset(file_location, skiprows, usecols)
    data.columns = ['col1', 'col2', 'col3', 'average']
    mean = mean_in_triplet(data, 'col1', 'col2', 'col3', 'average')
    p = max(probs_lambda)
    return binom.sf(mean - 1, complete, p)

if __name__ == "__main__":
    print("RTS colony p_value upper bound ", run_1('./data/OSF_Storage/Bishayee Colony Counts 10.27.97-3.8.01.csv',2, ["col1","col2","col3","average"], probs_lambda))
    print("Others colony p_value upper bound ", run_1('./data/OSF_Storage/Other Investigators in Lab.Colony Counts.4.23.92-11.27.02.csv',1,["col1","col2","col3","average"],probs_lambda))
    print("RTS colony (p_value, no_mean, no_expected, Sd, z, p_value_for_normal) = ", run('./data/OSF_Storage/Bishayee Colony Counts 10.27.97-3.8.01.csv',2, ["col1","col2","col3","average"], probs_lambda))
    print("Others colony (p_value, no_mean, no_expected, Sd, z, p_value_for_normal) = ", run('./data/OSF_Storage/Other Investigators in Lab.Colony Counts.4.23.92-11.27.02.csv',1,["col1","col2","col3","average"],probs_lambda))
    print("RTS coulter (p_value, no_mean, no_expected, Sd, z, p_value_for_normal) = ", run('./data/OSF_Storage/Bishayee Coulter Counts.10.20.97-7.16.01.csv', 1, ["Count 1", "Count 2", "Count 3", "Average"], probs_lambda))
    print("Others coulter (p_value, no_mean, no_expected, Sd, z, p_value_for_normal) = ", run('./data/OSF_Storage/Other Investigators in Lab.Coulter Counts.4.15.92-5.21.05.csv',1,["Coul 1","Coul 2","Coul 3","Average"], probs_lambda))
    print("Outside lab 1 coulter (p_value, no_mean, no_expected, Sd, z, p_value_for_normal) = ", run('./data/OSF_Storage/Outside Lab 1.Coulter Counts.6.7.91-4.9.99.csv',0,[1,2,3,4], probs_lambda))
    print("Outside lab 2 coulter (p_value, no_mean, no_expected, Sd, z, p_value_for_normal) = ", run('./data/OSF_Storage/Outside Lab 2.Coulter Counts.6.6.08-7.7.08.csv',1,["Count 1", "Count 2", "Count 3", "Average"], probs_lambda))
    print("Outside lab 3 colony (p_value, no_mean, no_expected, Sd, z, p_value_for_normal) = ", run('./data/OSF_Storage/Outside Lab 3.Colony Counts.2.4.10-5.21.12.csv',1,["c1", "c2", "c3", "average"], probs_lambda))


