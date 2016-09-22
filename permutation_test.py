from summary_stat import load_dataset, mean_in_triplet
from ChiSq import run2
from equaldigit import equal_digit_from_data
import pandas as pd
import numpy as np
from scipy.stats import binom

np.random.seed(0)
def load_all_data(list_of_inputs):
    combined_data = pd.DataFrame(columns=['col1', 'col2', 'col3', 'average'])
    list_of_sizes = []
    for single_input in list_of_inputs:
        (single_input_data, total, complete) = load_dataset(single_input[0], single_input[1], single_input[2])
        list_of_sizes.append(len(single_input_data))
        combined_data = combined_data.append(single_input_data)
    return (combined_data, list_of_sizes)

def sample_data(list_of_sizes, combined_data):
    shuffled_combined_data = combined_data.iloc[np.random.permutation(len(combined_data))]
    sum = 0
    list_of_sampled_data = []
    for i in list_of_sizes:
        df = shuffled_combined_data.iloc[sum:sum+i]
        sum = sum + i
        list_of_sampled_data.append(df)
    return list_of_sampled_data
    
def run_tests(list_of_sampled_data, list_of_names):
    for i in range(len(list_of_sampled_data)):
        sampled_data = list_of_sampled_data[i]
        mean_in_triplet_sample_data = mean_in_triplet(sampled_data,'col1','col2','col3','average')
        (manual_chi2, chi2, p, f_obs, tot) = run2(sampled_data)
        name = list_of_names[i]
        if "Coulter" in name:
            (greater, equal) = equal_digit_from_data(list_of_sampled_data[i])
            print(name, "(Mean in triplet, manual_chi_sq, chi_sq, p, f_obs, tot, "
                        "equal digit percentage, probability of equal digits greater than observed)"
                  , mean_in_triplet_sample_data, manual_chi2, chi2, p, f_obs, tot, greater / (equal * 1.0),
                  1 - binom.cdf(equal, greater, 0.1) + binom.pmf(equal, greater, 0.1))
        else:
            print(name, "(Mean in triplet, manual_chi_sq, chi_sq, p, f_obs, tot)"
                  , mean_in_triplet_sample_data, manual_chi2, chi2, p, f_obs, tot)

def run(list_of_inputs, list_of_names):
    (combined_data, list_of_sizes) = load_all_data(list_of_inputs)
    list_of_sampled_data = sample_data(list_of_sizes, combined_data)
    run_tests(list_of_sampled_data, list_of_names)

if __name__ == '__main__':
    list_of_inputs = (('./data/OSF_Storage/Bishayee Colony Counts 10.27.97-3.8.01.csv', 2, ["col1","col2","col3","average"]),
                      ('./data/OSF_Storage/Bishayee Coulter Counts.10.20.97-7.16.01.csv', 1,["Count 1", "Count 2", "Count 3", "Average"]),
                      ('./data/OSF_Storage/Other Investigators in Lab.Colony Counts.4.23.92-11.27.02.csv',1,["col1","col2","col3","average"]),
                      ('./data/OSF_Storage/Other Investigators in Lab.Coulter Counts.4.15.92-5.21.05.csv',1,["Coul 1","Coul 2","Coul 3","Average"]),
                      ('./data/OSF_Storage/Outside Lab 1.Coulter Counts.6.7.91-4.9.99.csv',0,[1,2,3,4]),
                      ('./data/OSF_Storage/Outside Lab 2.Coulter Counts.6.6.08-7.7.08.csv',1,["Count 1", "Count 2", "Count 3", "Average"]),
                      ('./data/OSF_Storage/Outside Lab 3.Colony Counts.2.4.10-5.21.12.csv',1,["c1", "c2", "c3", "average"]))
    list_of_names = ("RTS Colony", "RTS Coulter", "Others Colony", "Others Coulter", "Outside Lab 1 Coulter", "Outside Lab 2 Coulter", "Outside Lab 3 Colony")
    run(list_of_inputs, list_of_names)