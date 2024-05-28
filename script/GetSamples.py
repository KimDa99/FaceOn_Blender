import tarfile

file_path0 = 'FaceOn/data/part1.tar.gz'
file_path1 = 'FaceOn/data/part2.tar.gz'
file_path2 = 'FaceOn/data/part3.tar.gz'
extract_path = 'FaceOn/data'

with tarfile.open(file_path0, 'r:gz') as tar:
    tar.extractall(extract_path)
    print(f'Extracted {file_path0}')

with tarfile.open(file_path1, 'r:gz') as tar:
    tar.extractall(extract_path)
    print(f'Extracted {file_path1}')

with tarfile.open(file_path2, 'r:gz') as tar:
    tar.extractall(extract_path)
    print(f'Extracted {file_path2}')
