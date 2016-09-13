import pandas as pd

def load_data(filename, skiprows, usecols):
    data = pd.read_csv(filename, skiprows=skiprows, usecols=usecols)
    data.columns = ['col1', 'col2', 'col3']
    filtered_data = pd.DataFrame(columns=['col1', 'col2', 'col3'])
    complete = 0
    for index, row in data.iterrows():
        try:
            filtered_data = filtered_data.append({'col1': int(row['col1']), 'col2': int(row['col2']), 'col3': int(row['col3'])}, ignore_index=True)
            complete = complete + 1
        except ValueError:
            pass
    return (filtered_data, complete)

def equal_digit(filename, skiprows, usecols):
    (data, complete) = load_data(filename, skiprows, usecols)
    total = 0
    equal = 0
    for index, row in data.iterrows():
        if row['col1'] >= 100:
            total = total + 1
            digit_list = list(str(int(row['col1'])))
            if digit_list[len(digit_list) - 1] == digit_list[len(digit_list) - 2]:
                equal = equal + 1
        if row['col2'] >= 100:
            total = total + 1
            digit_list = list(str(int(row['col2'])))
            if digit_list[len(digit_list) - 1] == digit_list[len(digit_list) - 2]:
                equal = equal + 1
        if row['col3'] >= 100:
            total = total + 1
            digit_list = list(str(int(row['col3'])))
            if digit_list[len(digit_list) - 1] == digit_list[len(digit_list) - 2]:
                equal = equal + 1
    return total, equal


if __name__ == "__main__":

    (RTStotal, RTSequal) = equal_digit('./data/OSF_Storage/Bishayee Coulter Counts.10.20.97-7.16.01.csv', 1,
               ["Count 1", "Count 2", "Count 3"])
    (otherTotal, otherEqual) = equal_digit('./data/OSF_Storage/Other Investigators in Lab.Coulter Counts.4.15.92-5.21.05.csv', 1,
                ["Coul 1", "Coul 2", "Coul 3"])
    (outside2Total, outside2Equal) = equal_digit('./data/OSF_Storage/Outside Lab 2.Coulter Counts.6.6.08-7.7.08.csv', 1,
               ["Count 1", "Count 2", "Count 3"])
    (outside3Total, outside3Equal) = equal_digit('./data/OSF_Storage/Outside Lab 3.Colony Counts.2.4.10-5.21.12.csv', 1, ["c1", "c2", "c3"])

    print("RTS coulter (equal, total) = ", RTSequal, RTStotal)
    print("Others coulter (equal, total) = ", otherEqual + outside2Equal + outside3Equal, otherTotal + outside2Total + outside3Total)
    print ('equal digit percentage of RTS coulter = ', RTSequal / (RTStotal * 1.0))
    print ('equal digit percentage of others coulter = ', (otherEqual + outside2Equal + outside3Equal) / ((otherTotal + outside2Total + outside3Total) * 1.0))
