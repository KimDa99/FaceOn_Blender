import os
import numpy as np

def GetMeanOfPoints(indexes, points_path='FaceOn/data/combined_Normalized'):
    points = []
    colors = []

    for file in os.listdir(points_path):
        if file.endswith('.npy'):
            name = file.split('/')[-1][:-4]
            
            if name not in indexes:
                continue
            
            data = np.load(f'{points_path}/{file}')
            
            points.append(data[0][0])
            colors.append(data[1][0])

    points = np.array(points)
    colors = np.array(colors)

    mean_points = np.mean(points, axis=0)
    mean_colors = np.mean(colors, axis=0)

    return mean_points, mean_colors

def GetIndexes(path='FaceOn/data/min_max_file_names/browArchPosition/max.npy'):
    return np.load(path)

def SaveMeanInFile(indexes_path='FaceOn/data/min_max_file_names/browArchPosition', points_path = 'FaceOn/data/combined_Normalized',save_path='FaceOn/data/mean_points_colors'):

    for file in os.listdir(indexes_path):
        if file.endswith('.npy'):
            print(file)
            indexes = GetIndexes(f'{indexes_path}/{file}')
            # Get the name of each file name without the extension
            indexes = [index.split('.')[0] for index in indexes]

            print('indexes: ', indexes)
            mean_points, mean_colors = GetMeanOfPoints(indexes, points_path)
            print('mean_points:', mean_points)
            name = file[:-4]
            parts = indexes_path.split('/')[-1]

            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            np.save(f'{save_path}/{parts}_{name}_mean_points.npy', mean_points)
            np.save(f'{save_path}/{parts}_{name}_mean_colors.npy', mean_colors)
            print('means are saved')

def CaculateSaveBatch(path='FaceOn/data/min_max_file_names', points_path='FaceOn/data/combined_Normalized', save_path='FaceOn/data/means_points_colors'):
    print(path)
    for file in os.listdir(path):
        if os.path.isdir(f'{path}/{file}'):
            print(f'{path}/{file}')
            SaveMeanInFile(indexes_path=f'{path}/{file}', points_path=points_path, save_path=save_path)

def GetTotalMean(points_path='FaceOn/data/combined_Normalized'):
    points = []
    colors = []

    for file in os.listdir(points_path):
        if file.endswith('.npy'):
            data = np.load(f'{points_path}/{file}')
            points.append(data[0][0])
            colors.append(data[1][0])

    points = np.array(points)
    colors = np.array(colors)

    mean_points = np.mean(points, axis=0)
    mean_colors = np.mean(colors, axis=0)

    return mean_points, mean_colors

# CaculateSaveBatch(path='FaceOn/data/xyzNormalized/min_max_file_names', points_path='FaceOn/data/xyzNormalized/combined_Normalized', save_path='FaceOn/data/xyzNormalized/means_points_colors')
mean_points, mean_colors = GetTotalMean(points_path='FaceOn/data/xyzNormalized/combined_Normalized')
np.save('FaceOn/data/xyzNormalized/total_mean_points.npy', mean_points)
np.save('FaceOn/data/xyzNormalized/total_mean_colors.npy', mean_colors)
