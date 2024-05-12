import requests
import pandas as pd
import numpy as np
import os
import datetime


def create_directory(directory_path):
    print('ok')
    if os.path  .exists(directory_path):
        print(f"The directory '{directory_path}' already exists.")
        return True
    else:
        try:
            os.makedirs(directory_path)
            print(f"The directory '{directory_path}' has been created successfully.")
            return True
        except OSError as e:
            print(f"Failed to create directory '{directory_path}': {e}")
            return False


def create_data_frame(file_count, file_path):
    a = requests.get('https://api.frankfurter.app/latest?from=pln&to=USD,GBP,EUR')

    request_body = a.json()

    values = request_body.values()

    v = list(values)

    currency = v[-1]
    kkeys = list(currency.keys())
    kvalue = list(currency.values())
    timestamp = datetime.datetime.now()
    karray = np.array(['timestamp', v[1], kkeys[0], kkeys[1], kkeys[2]])
    kvarray = np.array([timestamp, v[0], kvalue[0], kvalue[1], kvalue[2]])

    df = pd.DataFrame(kvarray, karray)

    data = df.transpose()

    path: str = file_path
    filename: str = f'test{file_count + 1}.csv'
    full_path: str = os.path.join(path, filename)
    data.to_csv(full_path, sep=',', index=False, mode='w')

    print(f'file {full_path} has been created')


def count_files(dir_path):
    file_counter = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            file_counter += 1
    return file_counter


def remove_files(files_count, dir_path):

    file_dict = {}

    if files_count >= 7:
        for path in os.listdir(dir_path):
            pathl = os.path.join(dir_path, path)
            creation_time = os.path.getctime(pathl)

            file_dict[pathl] = creation_time

        file_to_delete = min(file_dict, key=file_dict.get)
        print(f'file to delete: {file_to_delete}')
        os.remove(file_to_delete)
        print(f'{file_to_delete} has been deleted')


dir_path1 = 'C:/Users/mateu/OneDrive/Pulpit/test/'


create_directory(dir_path1)

count = count_files(dir_path1)
print('current file count is: ', count)

# create_data_frame(count, dir_path1)
# remove_files(count, dir_path1)
