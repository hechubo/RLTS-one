import pandas as pd
import random

def merge_sorted_lists(list1, list2):
    index1, index2 = 0, 0
    merged_list = []

    while index1 < len(list1) and index2 < len(list2):
        if list1[index1] < list2[index2]:
            merged_list.append(list1[index1])
            index1 += 1
        elif list1[index1] > list2[index2]:
            merged_list.append(list2[index2])
            index2 += 1
        else:
            merged_list.append(list1[index1])
            index1 += 1
            index2 += 1

    while index1 < len(list1):
        merged_list.append(list1[index1])
        index1 += 1

    while index2 < len(list2):
        merged_list.append(list2[index2])
        index2 += 1

    return merged_list

def merge(T_1, T_2): 
    t_line = merge_sorted_lists([T_1[i][0] for i in range(len(T_1))], [T_2[i][0] for i in range(len(T_2))])
    all_t_line = range(min(T_1[0][0], T_2[0][0]), max(T_1[-1][0], T_2[-1][0]) + 1)
    dic_1 = {'time':[T_1[i][0] for i in range(len(T_1))], 'var':[T_1[i][1] for i in range(len(T_1))]}
    dic_2 = {'time':[T_2[i][0] for i in range(len(T_2))], 'var':[T_2[i][1] for i in range(len(T_2))]}
    dic_time = {'time':all_t_line}
    
    df1 = pd.DataFrame(dic_1)
    df2 = pd.DataFrame(dic_2)
    df1.set_index('time', inplace=True)
    df2.set_index('time', inplace=True)
    df_time = pd.DataFrame(dic_time)
    df_time.set_index('time', inplace=True)
    
    df1 = df1.reindex(df_time.index)
    df1_interpolated = df1.interpolate(method='linear')
    df1_value = df1_interpolated['var'].tolist()
    df2 = df2.reindex(df_time.index)
    df2_interpolated = df2.interpolate(method='linear')
    df2_value = df2_interpolated['var'].tolist()
    
    merged_T = [[t_line[i], (df1_value[all_t_line.index(t_line[i])], df2_value[all_t_line.index(t_line[i])])] for i in range(len(t_line))]
    
    return merged_T


numbers = range(1, 731)
random_numbers_1 = random.sample(numbers, 10)
random_numbers_2 = random.sample(numbers, 12)


column_names = ['latitude', 'longitude', 'timestamp']

df = pd.read_csv('0.txt', sep=' ', header=None, names=column_names)
random_1 = [0, 732] + random_numbers_1
random_2 = [0, 732] + random_numbers_2
random_1.sort()
random_2.sort()
T_1 = [[df['timestamp'][i], df['latitude'][i]] for i in random_1]
T_2 = [[df['timestamp'][i], df['longitude'][i]] for i in random_2]

print(merge(T_1, T_2))