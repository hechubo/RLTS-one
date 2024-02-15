import os
import random
import time

root_path = r'./TrajData/Geolife Trajectories 1.3/Data/'
out_path_1 = r'./TrajData/Geolife_out_1/'
out_path_2 = r'./TrajData/Geolife_out_2/'
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
    fw_1 = open(os.path.join(out_path_1, str(write_name)), 'w')
    fw_2 = open(os.path.join(out_path_2, str(write_name)), 'w')
    c = 0
    line_count = 0
    for line in f:
        if c < 6:
            c = c + 1
            continue
        temp = line.strip().split(',')
        if len(temp) < 7:
            continue
        longitude = temp[0]
        latitude = temp[1]
        timestamp = str(int(time.mktime(time.strptime(temp[5]+' '+temp[6], '%Y-%m-%d %H:%M:%S'))))
        fw_1.write(longitude + ' ' + timestamp + '\n')
        fw_2.write(latitude + ' ' + timestamp + '\n')
        line_count = line_count + 1
    f.close()
    fw_1.close()
    fw_2.close()
    if line_count <= 30:
        os.remove(os.path.join(out_path_1, str(write_name)))
        os.remove(os.path.join(out_path_2, str(write_name)))
        write_name = write_name - 1
    write_name = write_name + 1