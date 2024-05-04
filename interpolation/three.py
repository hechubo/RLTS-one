import numpy as np
import pandas as pd
from itertools import groupby
from operator import itemgetter

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

def merge(T_1, T_2,T_3): 
    t_line = [T_1[i][0] for i in range(len(T_1))] + [T_2[i][0] for i in range(len(T_2))]
    t_line =t_line + [T_3[i][0] for i in range(len(T_3))]
    t_line = list(set(t_line))
    t_line.sort()
    all_t_line = range(min(T_1[0][0], T_2[0][0], T_3[0][0]), max(T_1[-1][0], T_2[-1][0], T_3[-1][0]) + 1)
    dic_1 = {'time':[T_1[i][0] for i in range(len(T_1))], 'var':[T_1[i][1] for i in range(len(T_1))]}
    dic_2 = {'time':[T_2[i][0] for i in range(len(T_2))], 'var':[T_2[i][1] for i in range(len(T_2))]}
    dic_3 = {'time':[T_3[i][0] for i in range(len(T_3))], 'var':[T_3[i][1] for i in range(len(T_3))]}
    dic_time = {'time':all_t_line}

    df1 = pd.DataFrame(dic_1)
    df2 = pd.DataFrame(dic_2)
    df3 = pd.DataFrame(dic_3)
    df1.set_index('time', inplace=True)
    df2.set_index('time', inplace=True)
    df3.set_index('time', inplace=True)
    df_time = pd.DataFrame(dic_time)
    df_time.set_index('time', inplace=True)

    df1 = df1.reindex(df_time.index)
    df1_interpolated = df1.interpolate(method='linear')
    df1_value = df1_interpolated['var'].tolist()
    df2 = df2.reindex(df_time.index)
    df2_interpolated = df2.interpolate(method='linear')
    df2_value = df2_interpolated['var'].tolist()
    df3 = df3.reindex(df_time.index)
    df3_interpolated = df3.interpolate(method='linear')
    df3_value = df3_interpolated['var'].tolist()
    
    merged_T = [[t_line[i], (df1_value[all_t_line.index(t_line[i])], df2_value[all_t_line.index(t_line[i])], df3_value[all_t_line.index(t_line[i])])] for i in range(len(t_line))]
    
    return merged_T


df_alt = pd.read_csv('alt_after.txt', sep=' ',header=None)
df_alt = list(df_alt[0])
alt_list = []

for i in range(len(df_alt) // 2):
    alt_data = []
    alt_data.append(int(df_alt[2*i+1]))
    alt_data.append(df_alt[2*i])
    
    alt_list.append(alt_data)
alt_list.sort(key=lambda x:x[0])
alt_list_drop= []
for key, group in groupby(alt_list, key=itemgetter(0)):
    group_list = list(group)
    avg = sum(item[1] for item in group_list) / len(group_list)
    alt_list_drop.append((key, avg))

df_lat = pd.read_csv('lat_after.txt', sep=' ',header=None)
df_lat = list(df_lat[0])
lat_list = []

for i in range(len(df_lat) // 2):
    lat_data = []
    lat_data.append(int(df_lat[2*i+1]))
    lat_data.append(df_lat[2*i])
    
    lat_list.append(lat_data)
lat_list.sort(key=lambda x:x[0])
lat_list_drop= []
for key, group in groupby(lat_list, key=itemgetter(0)):
    group_list = list(group)
    avg = sum(item[1] for item in group_list) / len(group_list)
    lat_list_drop.append((key, avg))
    
df_lon = pd.read_csv('lon_after.txt', sep=' ',header=None)
df_lon = list(df_lon[0])
lon_list = []

for i in range(len(df_lon) // 2):
    lon_data = []
    lon_data.append(int(df_lon[2*i+1]))
    lon_data.append(df_lon[2*i])
    
    lon_list.append(lon_data)
lon_list.sort(key=lambda x:x[0])

lon_list_drop= []
for key, group in groupby(lon_list, key=itemgetter(0)):
    group_list = list(group)
    avg = sum(item[1] for item in group_list) / len(group_list)
    lon_list_drop.append((key, avg))
    
    
new_list = merge(lat_list_drop,lon_list_drop,alt_list_drop)

with open('my_list.txt', 'w') as file:
    for item in new_list:
        file.write(str(item) + '\n')

# random_1 = [0, 732] + random_numbers_1
# random_2 = [0, 732] + random_numbers_2
# random_1.sort()
# random_2.sort()
# T_1 = [[df['timestamp'][i], df['latitude'][i]] for i in random_1]
# T_2 = [[df['timestamp'][i], df['longitude'][i]] for i in random_2]

# print(merge(T_1, T_2))