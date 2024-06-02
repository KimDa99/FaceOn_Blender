import os
import numpy as np

def Get_names_values_colors(img_path, meanMaxMin_path = 'FaceOn/mean_max_min_02.txt', featureList_path = 'FaceOn/featureList/'):
    print("start")
    import DataProcess.GetLandmarks as GetLandmarks
    # img_path = 'final project/data/me_front.jpg'
    # img_path = 'FaceOn/data/xyzNormalized/examples/eyeBetween/max/52_26_1_2_20170116175511254.jpg'
    # img_path = 'FaceOn/data/xyzNormalized/examples/eyeBetween/min/53_30_0_0_20170117144022715.jpg'
    points, colors = GetLandmarks.GetPointsColor(img_path)

    print("normalize points")
    import DataProcess.normalizePoints as normalizePoints
    normalized_points = normalizePoints.normalizePoints(points)

    print("calculate features")
    import DataProcess.CalculateFeatures as CalculateFeatures
    features = CalculateFeatures.ExtractFeatures(normalized_points, colors, False)

    print("read mean, max and min values")
    # meanMaxMin_path = 'FaceOn/data/xyzNormalized/mean_max_min_02.txt'
    # read the mean, max and min values from the txt file
    meanValues = {}
    maxValues = {}
    minValues = {}
    with open(meanMaxMin_path, 'r') as f:
        for line in f:
            key, values = line.split(':')
            mean, max, min = values.split(',')
            meanValues[key] = float(mean)
            maxValues[key] = float(max)
            minValues[key] = float(min)

    print("normalize features: ")
    for key in features:
        if (key == 'file_name' or key == 'symmetry' or key == 'skinColor' or key == 'lipColor'):
            continue

        if (features[key] > meanValues[key]) :
            features[key] = (features[key] - meanValues[key]) / (maxValues[key] - meanValues[key])
        else:
            features[key] = (features[key] - meanValues[key]) / (meanValues[key] - minValues[key])

    lipColor = features['lipColor']
    skinColor = features['skinColor']
    names = []
    values = []
    for key in features:
        if key == 'file_name' or key == 'symmetry' or key == 'skinColor' or key == 'lipColor':
            continue
        names.append(key)
        values.append(features[key])


    print(features)

    print("saving features in a txt file")


    if not os.path.exists(featureList_path):
        os.makedirs(featureList_path)

    # save pictures
    image_path = featureList_path + img_path.split('/')[-1]
    import cv2
    cv2.imwrite(image_path, cv2.imread(img_path))

    # save the features in a txt file
    path = featureList_path + img_path.split('/')[-1].split('.')[0] + '.txt'
    with open(path, 'w') as f:
        f.write('names = [')
        for key in features:
            if key == 'file_name' or key == 'symmetry' or key == 'skinColor' or key == 'lipColor':
                continue
            f.write(f'"{key}", ')
        f.write(']\n')
        
        f.write('values = [')
        for key in features:
            if key == 'file_name' or key == 'symmetry' or key == 'skinColor' or key == 'lipColor':
                continue
            f.write(f'{features[key]}, ')
        f.write(']\n')

        #save form of [value, value, ...]
        f.write('skinColor = [')
        for i in range(len(features['skinColor'])):
            f.write(f'{features["skinColor"][i]}, ')
        f.write(']\n')

        f.write('lipColor = [')
        for i in range(len(features['lipColor'])):
            f.write(f'{features["lipColor"][i]}, ')
        f.write(']\n')

    
    return names, values, skinColor, lipColor

image_path = 'your_image_path'    
saving_path = 'your_saving_path'
Get_names_values_colors(image_path, featureList_path=saving_path)

'''
# Batch processing example
path = 'FaceOn/samples'
for file in os.listdir(path):
    if file.endswith('.jpg'):
        Get_names_values_colors(f'{path}/{file}', featureList_path=saving_path)
'''