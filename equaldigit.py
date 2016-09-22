import pandas as pd
from scipy.stats import binom

def load_data(filename, skiprows, usecols):
    data = pd.read_csv(filename, skiprows=skiprows, usecols=usecols)
    data.columns = ['col1', 'col2', 'col3']
    filtered_data = pd.DataFrame(columns=['col1', 'col2', 'col3'])
    complete = 0
    total = 0
    for index, row in data.iterrows():
        try:
            max_value = max(int(row['col1']), int(row['col2']), int(row['col3']))
            min_value = min(int(row['col1']), int(row['col2']), int(row['col3']))
            if (max_value - min_value >= 2):
                filtered_data = filtered_data.append({'col1':int(row['col1']), 'col2':int(row['col2']), 'col3':int(row['col3'])},ignore_index=True)
                complete = complete + 1
            total = total + 1
        except ValueError:
            pass
    return (filtered_data, complete, total)

def equal_digit(filename, skiprows, usecols):
    (data, complete, total) = load_data(filename, skiprows, usecols)
    (greater, equal) = equal_digit_from_data(data)
    return (greater, equal)

def equal_digit_from_data(data):
    greater = 0
    equal = 0
    for index, row in data.iterrows():
        if row['col1'] >= 100:
            greater = greater + 1
            digit_list = list(str(int(row['col1'])))
            if digit_list[len(digit_list) - 1] == digit_list[len(digit_list) - 2]:
                equal = equal + 1
        if row['col2'] >= 100:
            greater = greater + 1
            digit_list = list(str(int(row['col2'])))
            if digit_list[len(digit_list) - 1] == digit_list[len(digit_list) - 2]:
                equal = equal + 1
        if row['col3'] >= 100:
            greater = greater + 1
            digit_list = list(str(int(row['col3'])))
            if digit_list[len(digit_list) - 1] == digit_list[len(digit_list) - 2]:
                equal = equal + 1
    return greater, equal

if __name__ == "__main__":

    (RTSgreater, RTSequal) = equal_digit('./data/OSF_Storage/Bishayee Coulter Counts.10.20.97-7.16.01.csv', 1,
               ["Count 1", "Count 2", "Count 3"])
    (otherGreater, otherEqual) = equal_digit('./data/OSF_Storage/Other Investigators in Lab.Coulter Counts.4.15.92-5.21.05.csv', 1,
                ["Coul 1", "Coul 2", "Coul 3"])
    (outside2Greater, outside2Equal) = equal_digit('./data/OSF_Storage/Outside Lab 2.Coulter Counts.6.6.08-7.7.08.csv', 1,
               ["Count 1", "Count 2", "Count 3"])
    (outside1Greater, outside1Equal) = equal_digit('./data/OSF_Storage/Outside Lab 1.Coulter Counts.6.7.91-4.9.99.csv', 0, [1, 2, 3])

    print("RTS coulter (equal, total) = ", RTSequal, RTSgreater)
    print("Others coulter (equal, total) = ", otherEqual + outside2Equal + outside1Equal, otherGreater + outside2Greater + outside1Greater)
    print("Other investigator in lab (equal, total) = ", otherEqual, otherGreater)
    print("Outside lab 1 (equal, total) = ", outside1Greater, outside1Equal)
    print("Outside lab 2 (equal, total) = ", outside2Equal, outside2Greater)
    print("\n")


    print ('equal digit percentage of RTS coulter = ', RTSequal / (RTSgreater * 1.0))
    print ('equal digit percentage of others coulter = ', (otherEqual + outside2Equal + outside1Equal) / ((otherGreater + outside2Greater + outside1Greater) * 1.0))
    print ('equal digit percentage of other investigator in lab = ', otherEqual / (otherGreater * 1.0))
    print ('equal digit percentage of outside lab1 = ', outside1Equal / (outside1Greater * 1.0))
    print ('equal digit percentage of outside lab2 = ', outside2Equal / (outside2Greater * 1.0))
    print("\n")


    print ('probability of number of equal digits greater than the boundary of RTS coulter is', 1 - binom.cdf(RTSequal, RTSgreater, 0.1) + binom.pmf(RTSequal, RTSgreater, 0.1))
    print ('probability of number of equal digits greater than the boundary of other coulter is',
           1 - binom.cdf(otherEqual + outside2Equal + outside1Equal - 1, otherGreater + outside2Greater + outside1Greater, 0.1))
    print ('probability of number of equal digits greater than the boundary of other investigator in lab is',
           1 - binom.cdf(otherEqual - 1, otherGreater, 0.1))
    print ('probability of number of equal digits less than the boundary of outside lab1 is',
           1 - binom.cdf(outside1Equal - 1, outside1Greater, 0.1))
    print ('probability of number of equal digits less than the boundary of outside lab2 is',
           1 - binom.cdf(outside2Equal - 1, outside2Greater, 0.1))
    print("\n")

    print ('probability of number of equal digits greater than the boundary of the RTS coulter in the paper is', 1 - binom.cdf(635, 5155, 0.1))
    print ('probability of number of equal digits greater than the boundary of the other investigator coulter in the paper is',  1 - binom.cdf(290, 2942, 0.1))

