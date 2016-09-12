import pandas as pd

def load_dataset(filename, skiprows, usecols):
    data = pd.read_csv(filename,skiprows=skiprows, usecols=usecols)
    data.columns = ['col1', 'col2', 'col3', 'average']
    filtered_data = pd.DataFrame(columns=['col1', 'col2', 'col3', 'average'])
    for index, row in data.iterrows():
        try:
            filtered_data = filtered_data.append({'col1':int(row['col1']), 'col2':int(row['col2']), 'col3':int(row['col3']), 'average':float(row['average'])},ignore_index=True)
        except ValueError:
            pass
    return filtered_data

def num_complete(data, col1, col2, col3, average):
    complete = 0
    total = 0
    contains_mean = 0
    for index, row in data.iterrows():
        list_values = (int(row[col1]), int(row[col2]), int(row[col3]))
        mean = int(round(int(row[average])))
        max_value = max(int(row[col1]),int(row[col2]), int(row[col3]))
        min_value = min(int(row[col1]),int(row[col2]), int(row[col3]))
        if (max_value - min_value >= 2):
            complete+=1
            if (mean in list_values):
                contains_mean += 1
        total+=1
    return (complete, total, contains_mean)

def run(file_location, skiprows, usecols):
    data = load_dataset(file_location, skiprows, usecols)
    data.columns = ['col1','col2','col3','average']
    (complete, total, contains_mean) = num_complete(data, 'col1', 'col2','col3', 'average')
    return (complete, total, contains_mean)

if __name__ == "__main__":
    print ("RTS colony (complete, total, mean present) = ", run('./data/OSF_Storage/Bishayee Colony Counts 10.27.97-3.8.01.csv', 2, ["col1","col2","col3","average"]))
    print ("RTS coulter (complete, total, mean present) = ", run('./data/OSF_Storage/Bishayee Coulter Counts.10.20.97-7.16.01.csv', 1, ["Count 1", "Count 2", "Count 3", "Average"]))
    print ("Others colony (complete, total, mean present) = ", run('./data/OSF_Storage/Other Investigators in Lab.Colony Counts.4.23.92-11.27.02.csv',1,["col1","col2","col3","average"]))
    print ("Others coulter (complete, total, mean present) = ", run('./data/OSF_Storage/Other Investigators in Lab.Coulter Counts.4.15.92-5.21.05.csv',1,["Coul 1","Coul 2","Coul 3","Average"]))
    print ("Outside lab 1 colony (complete, total, mean present) = ", run('./data/OSF_Storage/Outside Lab 1.Coulter Counts.6.7.91-4.9.99.csv',0,[1,2,3,4]))
    print ("Outside lab 2 coulter (complete, total, mean present) = ", run('./data/OSF_Storage/Outside Lab 2.Coulter Counts.6.6.08-7.7.08.csv',1,["Count 1", "Count 2", "Count 3", "Average"]))
    print ("Outside lab 3 coulter (complete, total, mean present) = ", run('./data/OSF_Storage/Outside Lab 3.Colony Counts.2.4.10-5.21.12.csv',1,["c1", "c2", "c3", "average"]))