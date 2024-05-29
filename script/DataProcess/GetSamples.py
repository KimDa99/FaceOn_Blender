import tarfile
import os

def OpenTarGz(file_path, extract_path):
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(extract_path)
        print(f'Extracted {file_path}')

def MoveFiles(source_path, target_path):
    for file in os.listdir(source_path):
        os.rename(f'{source_path}/{file}', f'{target_path}/{file}')
    # remove the empty folder
    os.rmdir(source_path)

def removeUnderAgeFiles(path):
    for file in os.listdir(path):
        if file.startswith('under_age'):
            os.remove(f'{path}/{file}')
            print(f'{path}/{file} removed')
