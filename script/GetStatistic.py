import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

def load_dict(path):
    pickle_in = open(path, "rb")
    return pickle.load(pickle_in)


def removeOutliersNoises(values):
    # Calculate quartiles
    q1 = np.percentile(values, 2)
    q3 = np.percentile(values, 98)
    
    # Calculate IQR
    iqr = q3 - q1
    
    # Define lower and upper bounds
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # Remove outliers
    filtered_values = [v for v in values if v >= lower_bound and v <= upper_bound]
    
    return filtered_values


def normalizeData(values):
    # Max value: 1, Min value: 0
    max_val = np.max(values)
    min_val = np.min(values)

    # Normalize values
    normalized_values = [(v - min_val) / (max_val - min_val) for v in values]

    return normalized_values

def GetMinMaxIndex(values):
    min_val = np.min(values)
    max_val = np.max(values)
    min_index = values.index(min_val)
    max_index = values.index(max_val)
    return min_index, max_index

def GetMinMaxIndexes(values, n=5):
    # get top 5 min and max values
    min_indexes = []
    max_indexes = []

    for i in range(n):
        min_val = np.min(values)
        max_val = np.max(values)

        min_index = values.index(min_val)
        max_index = values.index(max_val)

        min_indexes.append(min_index)
        max_indexes.append(max_index)

        copiedValues = values.copy()
        copiedValues = np.array(copiedValues)
        mean = copiedValues.mean()
        values[min_index] = mean
        values[max_index] = mean

    return min_indexes, max_indexes

def showPlt(values, key):
    # Plot values as dots
    plt.plot(values, 'bo', markersize=3)  # 'bo' specifies blue dots
    plt.title(f'{key} Distribution')
    plt.xlabel('Index')
    plt.ylabel(key)
    
    # Calculate statistics
    mean_val = np.mean(values)
    max_val = np.max(values)
    min_val = np.min(values)
    median_val = np.median(values)
    variance_val = np.var(values)
    range_val = max_val - min_val
    std_deviation_val = np.std(values)
    
    # Add statistics to plot
    plt.text(0.5, 0.9, f'Mean: {mean_val:.2f}', ha='center', va='center', transform=plt.gca().transAxes)
    plt.text(0.5, 0.85, f'Max: {max_val:.2f}', ha='center', va='center', transform=plt.gca().transAxes)
    plt.text(0.5, 0.8, f'Min: {min_val:.2f}', ha='center', va='center', transform=plt.gca().transAxes)
    plt.text(0.5, 0.75, f'Median: {median_val:.2f}', ha='center', va='center', transform=plt.gca().transAxes)
    plt.text(0.5, 0.7, f'Variance: {variance_val:.2f}', ha='center', va='center', transform=plt.gca().transAxes)
    plt.text(0.5, 0.65, f'Range: {range_val:.2f}', ha='center', va='center', transform=plt.gca().transAxes)
    plt.text(0.5, 0.6, f'Standard Deviation: {std_deviation_val:.2f}', ha='center', va='center', transform=plt.gca().transAxes)
    
    plt.show()


def GetImagePath(file_name):
    return 'FaceOn/data/samples/' + file_name.replace('.pickle', '.jpg')

def SaveImage(source_path, target_path, order = -1):
    img = cv.imread(source_path)
    source_name = source_path.split('/')[-1]
    if img is None:
        print(f'Image is None: {source_path}')
        return

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    target_path = target_path + '/' + str(order) + '_'+source_name

    cv.imwrite(target_path, img)


dicts = load_dict('FaceOn/data/xyzNormalized/Gathered_Features.pickle')
dicts = dicts.copy()


def GetMostMeanPictures(dicts, percent = 0.3):
    meanPicturesFileNames = []
    for key in dicts:
        if key == 'fileNames' or key == 'skinColor' or key == 'lipColor' or key == 'symmetry':
            continue
        
        values = dicts[key]
        values = normalizeData(values)

        # get median pictures indexes if it is in the range
        print(len(values))
        n =  (0.5 - percent)* len(values)
        n = int(n)
        print(n)
        min_indexes, max_indexes = GetMinMaxIndexes(values, n)
        indexes = [i for i in range(len(values))]
        print(f'len: {len(indexes)}')
        indexes = [i for i in indexes if i not in min_indexes and i not in max_indexes]
        print(f'len: {len(indexes)}')

        fileNames = [dicts['fileNames'][i] for i in indexes]
        print(f'len: {len(fileNames)}')
        if meanPicturesFileNames == []:
            meanPicturesFileNames = fileNames
        else:
            #only if the file name is in the previous list
            meanPicturesFileNames = [name for name in meanPicturesFileNames if name in fileNames]
        
        print(f'key: {key}, len: {len(meanPicturesFileNames)}')
    
    return meanPicturesFileNames
    
# meanPicturesFileNames = GetMostMeanPictures(dicts)
# for i in range(len(meanPicturesFileNames)):
#     SaveImage(GetImagePath(meanPicturesFileNames[i]), 'FaceOn/data/xyzNormalized/examples/mean', i)

def GetMeanMaxMinValues(dicts):
    meanValues = {}
    maxValues = {}
    minValues = {}
    for key in dicts:
        if key == 'fileNames' or key == 'skinColor' or key == 'lipColor' or key == 'symmetry':
            continue
        
        values = dicts[key]

        meanValues[key] = np.median(values)
        
        # Get 2% of the values' mean
        n = 0.02 * len(values)
        n = int(n)
        vals = values.copy()
        min_indexes, max_indexes = GetMinMaxIndexes(vals, n)
        # print(f'{key} min_indexes: {min_indexes}')
        # print(f'{key} max_indexes: {max_indexes}')

        min = [values[i] for i in min_indexes]
        minValues[key] = np.median(min)

        max = [values[i] for i in max_indexes]
        maxValues[key] = np.median(max)
        print(f'{key} mean: {meanValues[key]}, max: {maxValues[key]}, min: {minValues[key]}')
    
    return meanValues, maxValues, minValues

meanValues, maxValues, minValues = GetMeanMaxMinValues(dicts)
# save in txt file the mean, max and min values
with open('FaceOn/data/xyzNormalized/mean_max_min_02.txt', 'w') as f:
    for key in meanValues:
        f.write(f'{key}: {meanValues[key]}, {maxValues[key]}, {minValues[key]}\n')


# for key in dicts:
#     if key == 'fileNames' or key == 'skinColor' or key == 'lipColor' or key == 'symmetry':
#         continue
    
#     values = dicts[key]
#     values = normalizeData(values)

#     n = (1/100) * len(values)
#     n = int(n)
#     print(n)
#     min_indexes, max_indexes = GetMinMaxIndexes(values, n)

#     min_paths = []
#     max_paths = []

#     path = 'FaceOn/data/xyzNormalized/examples/'+ key
#     min_path = path + '/min'
#     max_path = path + '/max'
    
#     if not os.path.exists('FaceOn/data/xyzNormalized/examples'):
#         os.makedirs('FaceOn/data/xyzNormalized/examples')

#     for i in range(n):
#         SaveImage(GetImagePath(dicts['fileNames'][min_indexes[i]]), min_path, i)
#         SaveImage(GetImagePath(dicts['fileNames'][max_indexes[i]]), max_path, i)
    
#     min_file_names = [dicts['fileNames'][i] for i in min_indexes]
#     max_file_names = [dicts['fileNames'][i] for i in max_indexes]

#     # save min and max file names as numpy files
#     target_path = 'FaceOn/data/min_max_file_names/'
#     if not os.path.exists(target_path):
#         os.makedirs(target_path)

#     target_path = 'FaceOn/data/min_max_file_names/' + key + '/'
#     if not os.path.exists(target_path):
#         os.makedirs(target_path)

#     np.save(target_path + 'min.npy', min_file_names)
#     np.save(target_path + 'max.npy', max_file_names)

#     showPlt(dicts[key], key)
#     # values = removeOutliersNoises(dicts[key])        

#     # showPlt(values, f'Normalized {key}')

#     cv.waitKey(0)