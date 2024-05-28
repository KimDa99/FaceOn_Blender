import os
import numpy as np

def findFileWithSuffix(path, suffix):
    for file in os.listdir(path):
        if file.endswith(suffix):
            return file
    return None

def combineTwoNp(normalizedPoints_file_path, color_file_path):
    combined = []
    normalizedPoints = np.load(normalizedPoints_file_path)
    colors = np.load(color_file_path)
    combined.append([normalizedPoints])
    combined.append([colors])
    return combined

def combineNormalizedPoints( normalizedPoints_files_path, color_files_path, target_path):
    for files in os.listdir(normalizedPoints_files_path):
        if files.endswith('_normalized.npy'):
            base_filename = files[:files.rfind('_')]
            color_file = findFileWithSuffix(color_files_path, f'{base_filename}_color.npy')
            if color_file is None:
                print(f'Error: No color file found for {files}')
                continue
            combined = combineTwoNp(f'{normalizedPoints_files_path}/{files}', f'{color_files_path}/{color_file}')
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            np.save(f'{target_path}/{base_filename}_combined.npy', combined)
            print(f'{target_path}/{base_filename}_combined.npy saved')

#combineNormalizedPoints('FaceOn/data/normalized/part1', 'FaceOn/data/landmarks/part1', 'FaceOn/data/combined_Normalized/part1')
combineNormalizedPoints('FaceOn/data/normalized/part2', 'FaceOn/data/landmarks/part2', 'FaceOn/data/combined_Normalized/part2')
combineNormalizedPoints('FaceOn/data/normalized/part3', 'FaceOn/data/landmarks/part3', 'FaceOn/data/combined_Normalized/part3')