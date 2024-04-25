import os
import random
import time

root_path = r'./TrajData/routes_clean/'
out_path_lon = r'./TrajData/routes_clean_lon/'
out_path_lat = r'./TrajData/routes_clean_lat/'
out_path_alt = r'./TrajData/routes_clean_alt/'
file_list = []
dir_list = []

def get_file_path(root_path, file_list, dir_list):
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        dir_file_path = os.path.join(root_path, dir_file)
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            get_file_path(dir_file_path, file_list, dir_list)
        else:
            file_list.append(dir_file_path)

get_file_path(root_path, file_list, dir_list)
random.shuffle(file_list)

write_name = 0

for fl in file_list:
    if write_name % 100 == 0:
        print('preprocessing ', write_name)
    f = open(fl)
    fw_lon = open(out_path_lon + str(write_name), 'w')
    fw_lat = open(out_path_lat + str(write_name), 'w')
    fw_alt = open(out_path_alt + str(write_name), 'w')
    line_count = 0
    alt_neg_count = 0
    for line in f:
        temp = line.strip().split()
        if len(temp) < 4:
            continue
        timestamp = int(temp[2]) // 1000  # Convert milliseconds to seconds
        fw_lon.write(temp[0] + ' ' + str(timestamp) + '\n')
        fw_lat.write(temp[1] + ' ' + str(timestamp) + '\n')
        fw_alt.write(temp[3] + ' ' + str(timestamp) + '\n')
        line_count += 1
        if float(temp[3]) == -1.0:
            alt_neg_count += 1
        else:
            alt_neg_count = 0
        if alt_neg_count >= 10:
            break
    f.close()
    fw_lon.close()
    fw_lat.close()
    fw_alt.close()
    if line_count <= 30 or alt_neg_count >= 10:
        os.remove(out_path_lon + str(write_name))
        os.remove(out_path_lat + str(write_name))
        os.remove(out_path_alt + str(write_name))
        write_name -= 1
    write_name += 1