from scipy.stats import poisson
import math
import numpy as np
import csv

# Define a function to compute the probability when a triplet contains its mean for lambda, and the result will be stored
# in the vector probs.
def prob(probs, number_of_values):
    for i in range(number_of_values):
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
        print probs[i]
    return probs

if __name__ == '__main__':
    number_of_values = 2081
    probs_lambda = prob(np.array([0.0] * number_of_values), number_of_values)
    with open('./data/probs_lambda.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(len(probs_lambda)):
            writer.writerow([probs_lambda[i]])