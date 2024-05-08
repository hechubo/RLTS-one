import numpy as np
import pandas as pd
from itertools import groupby
from operator import itemgetter

def merge(T_list): 
    '''
    传入列表的列表元素数量应与维度对应，元素应为时间序列
    '''
    t_line = []
    for T_i in T_list:
        t_line += [T_i[i][0] for i in range(len(T_i))]
    t_line = list(set(t_line))
    t_line.sort()
    
    all_t_line = range(min([T_i[0][0] for T_i in T_list]), max([T_i[-1][0] for T_i in T_list]) + 1)
    dic_time = {'time':all_t_line}
    df_time = pd.DataFrame(dic_time)
    df_time.set_index('time', inplace=True)
    
    interpolated_list = []
    for T_i in T_list:
        
        dic_i = {'time':[T_i[i][0] for i in range(len(T_i))], 'var':[T_i[i][1] for i in range(len(T_i))]}

        dfi = pd.DataFrame(dic_i)
        dfi.set_index('time', inplace=True)
        
        dfi = dfi.reindex(df_time.index)
        dfi_interpolated = dfi.interpolate(method='linear')
        dfi_value = dfi_interpolated['var'].tolist()
        interpolated_list.append(dfi_value)

    
    merged_T = [[t_line[i], [interpolated_list[j][all_t_line.index(t_line[i])] for j in range(len(T_list))]] for i in range(len(t_line))]
    
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
    
    
new_list = merge([lat_list_drop,lon_list_drop,alt_list_drop])

with open('my_list_nd.txt', 'w') as file:
    for item in new_list:
        file.write(str(item) + '\n')