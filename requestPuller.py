import argparse
import requests
import pandas as pd
import numpy as np
import os
import datetime


def create_directory(directory_path):
    if os.path.exists(directory_path):
        print(f"The directory '{directory_path}' already exists")
        return True
    else:
        try:
            os.makedirs(directory_path)
            print(f"The directory '{directory_path}' has been created successfully")
            return True
        except OSError as e:
            print(f"Failed to create directory '{directory_path}': {e}")
            return False


def create_data_frame(file_path):
    response = requests.get('https://api.frankfurter.app/latest?from=pln&to=USD,GBP,EUR')

    if response.status_code == 200:
        request_body = response.json()
        values = request_body.values()

        v = list(values)

        timestamp = datetime.datetime.now()

        currency = v[-1]
        kkeys = list(currency.keys())
        kvalue = list(currency.values())

        karray = np.array(['timestamp', v[1], kkeys[0], kkeys[1], kkeys[2]])
        kvarray = np.array([timestamp, v[0], kvalue[0], kvalue[1], kvalue[2]])

        df = pd.DataFrame(kvarray, karray)

        timestamp_str = timestamp.strftime("%Y%m%d%H%M%S").replace(":", "_")

        data = df.transpose()

        path: str = file_path
        filename: str = f'test{timestamp_str}.csv'
        full_path: str = os.path.join(path, filename)
        data.to_csv(full_path, sep=',', index=False, mode='w')

        print(f'file {full_path} has been created')
    else:
        print(f"Failed to fetch data from API. Status code: '{response.status_code}'")


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


def main(directory_path):
    create_directory(directory_path)
    count = count_files(directory_path)
    create_data_frame(directory_path)
    remove_files(count, directory_path)
    print(f'current file count inside {directory_path} is {count}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch currency exchange rates and manage CSV files')
    parser.add_argument('directory_path', help='Path to the directory to save CSV files')

    args = parser.parse_args()

    main(args.directory_path)
