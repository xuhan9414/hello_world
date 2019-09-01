import os


def ceate_str_to_txt(time_path,date):
    path_file_name = 'D:/auto_test_record/time_log_{}.txt'.format(time_path)
    if not os.path.exists(path_file_name):
        with open(path_file_name,'w') as f:
            print(f)
    with open (path_file_name,'a') as f:
        f.write(date + '\n')