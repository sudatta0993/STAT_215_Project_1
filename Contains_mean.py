import math
import scipy
from scipy.stats import poisson
from scipy.stats import binom
from scipy.stats import norm
import numpy as np
import pandas as pd
from summary_stat import load_dataset
from summary_stat import mean_in_triplet

# Define a function to compute the probability when a triplet contains its mean for lambda = (0, 1, 2, ..., 2000), and the result will be stored
# in the vector probs.
def prob(probs):
    for i in range(2001):
        n = poisson.ppf(1 - math.pow(10, -9), i)
        n = n.astype(int)
        sum = 0
        tempar = np.array([0.0] * (n + 1)) # use an array to store the pmf of poisson(lambda)
        tempar[i] = poisson.pmf(i, i) # start with the peak p(X = lambda)
        tempar[0] = poisson.pmf(0, i)
        for i1 in range(i - 1, 0, -1):
            tempar[i1] = tempar[i1 + 1] * (float(i1 + 1) / float(i)) # Compute p(X = lambda') where lambda' < lambda
        for i2 in range(i + 1, n + 1):
            tempar[i2] = tempar[i2 - 1] * (float(i) / float(i2)) # Compute p(X = lambda') where lambda' < lambda
        for j in range(2, n + 1):
            odd = int(j % 2 == 1)
            for k in range(j, n + 1):
                sum += 6 * tempar[k - j] * (tempar[k - int(j / 2)] + odd * tempar[k - int(j / 2) - 1]) * tempar[k]
        probs[i] = sum
        print("lambda is : ", i, "probability is : ", sum)
    return probs

# Compute the table of probability when lambda = 0, 1, 2, ..., 2000
probs_lambda = np.array([0.0] * 2001)
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
    # Initialize prob = 0 to each triplet
    probs = np.array([0.0] * len(mean))
    # Assign prob to each triplet
    for i in range(len(mean)):
        probs[i] = float(probs_lambda[int(mean[i])])
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

if __name__ == "__main__":
    print("RTS colony p_value upper bound ", binom.sf(689, 1343, 0.42))
    print("Others colony p_value upper bound ", binom.sf(108, 572, 0.42))
    print("RTS colony (p_value, no_mean, no_expected, Sd, z, p_value_for_normal) = ", run('./data/OSF_Storage/Bishayee Colony Counts 10.27.97-3.8.01.csv',2, ["col1","col2","col3","average"], probs_lambda))
    print("Others colony (p_value, no_mean, no_expected, Sd, z, p_value_for_normal) = ", run('./data/OSF_Storage/Other Investigators in Lab.Colony Counts.4.23.92-11.27.02.csv',1,["col1","col2","col3","average"],probs_lambda))

