import os
import random
import time
'''
将原始的GPS轨迹数据转换为一个更简洁、更易于后续处理的格式。
结果文件中的每一行包含一个经度、一个纬度和一个时间戳，这些数据均以空格分隔。
'''
root_path = r'./TrajData/Geolife Trajectories 1.3/Data/'
out_path = r'./TrajData/Geolife_out/'
out_path_1 = r'./TrajData/Geolife_out_1/'
out_path_2 = r'./TrajData/Geolife_out_2/'
file_list = []
dir_list = []

def get_file_path(root_path,file_list,dir_list):
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        dir_file_path = os.path.join(root_path,dir_file)
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            get_file_path(dir_file_path,file_list,dir_list)
        else:
            file_list.append(dir_file_path)


get_file_path(root_path, file_list, dir_list)

random.shuffle(file_list)

write_name = 0

for fl in file_list:
    if write_name % 100 == 0:
        print('preprocessing ', write_name)
    f = open(fl)
    fw = open(out_path + str(write_name), 'w')
    c = 0
    line_count = 0
    for line in f:
        if c < 6:
            c = c + 1
            continue
        temp = line.strip().split(',')
        if len(temp) < 7:
            continue
        fw.write(temp[0]+' '+temp[1]+' '+str(int(time.mktime(time.strptime(temp[5]+' '+temp[6],'%Y-%m-%d %H:%M:%S'))))+'\n')
        line_count = line_count + 1
    f.close()
    fw.close()
    if line_count <= 30:
        os.remove(out_path + str(write_name))
        write_name = write_name - 1
    write_name = write_name + 1    