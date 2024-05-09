import requests
import pandas as pd
import numpy as np
import os
import datetime


def CreateDataframe(fileCount, filePath):
    a = requests.get('https://api.frankfurter.app/latest?from=pln&to=USD,GBP,EUR')

    request_Body = a.json()

    values = request_Body.values()

    v = list(values)

    currency = v[-1]
    kkeys = list(currency.keys())
    kvalue = list(currency.values())
    timestamp = datetime.datetime.now()
    karray = np.array(['timestamp', v[1], kkeys[0], kkeys[1], kkeys[2]])
    kvarray = np.array([timestamp, v[0], kvalue[0], kvalue[1], kvalue[2]])

    df = pd.DataFrame(kvarray, karray)

    data = df.transpose()

    path: str = filePath
    filename: str = f'test{fileCount + 1}.csv'
    full_path: str = os.path.join(path, filename)
    data.to_csv(full_path, sep=',', index=False, mode='w')

    print(f'file {full_path} has been created')


def CountFile(dir_path):
    fileCounter = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            fileCounter += 1
    return fileCounter


def RemoveFile(count, dirPath):

    dict = {}

    if count >= 7:
        for path in os.listdir(dir_path):
            pathl = os.path.join(dirPath, path)
            creationTime = os.path.getctime(pathl)

            dict[pathl] = creationTime


        fileToDelete = min(dict, key=dict.get)
        print(f'file to delete: {fileToDelete}')
        os.remove(fileToDelete)
        print(f'{fileToDelete} has been deleted')


dir_path = 'C:/Users/mateu/OneDrive/Pulpit/test/'

count = CountFile(dir_path)

print('current file count is: ', count)

CreateDataframe(count, dir_path)
RemoveFile(count, dir_path)
