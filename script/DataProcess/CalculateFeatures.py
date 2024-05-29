import os
import numpy as np
import mediapipe as mp
try:
    from sklearn.cluster import KMeans  # pip install scikit-learn
except ImportError as e:
    print(f'Failed to import scikit-learn: {e}')
import pickle

# Eyes
eye_front_right_index = 133
eye_front_left_index = 362
eye_back_right_index = 33
eye_back_left_index = 263

eye_top_left_index = 386
eye_top_right_index = 159
eye_bottom_left_index = 374
eye_bottom_right_index = 145

eye_above_right_indexes = [161, 160, 159, 158, 157]
eye_above_left_indexes = [384, 385, 386, 387, 388]
eye_below_right_indexes = [163, 144, 145, 153, 154]
eye_below_left_indexes = [390, 373, 374, 380, 381]

# brows
brow_start_left_indexs = [336, 285]
brow_arch_left_indexs = [334, 282]
brow_end_left_indexs = [300, 276]
brow_start_right_indexs = [107, 55]
brow_arch_right_indexs = [105, 52]
brow_end_right_indexs = [70, 46]

# lips
top_lip_indexes = [ 61, 78, 185, 191, 40,
                    80, 39, 81, 37, 82, 
                    0, 13, 267, 312, 269, 
                    311, 270, 310, 409, 415, 
                    291, 308]

bottom_lip_indexes = [ 61, 146, 91, 181, 84,
                      17, 314, 405, 321, 375,
                      291, 308, 324, 318, 402,
                      317, 14, 87, 178, 88,
                      95, 78]

top_lip_top_index = 0
top_lip_bottom_index = 13
bottom_lip_top_index = 14
bottom_lip_bottom_index = 17
lip_right_end_index = 61
lip_left_end_index = 291

# Nose
nose_bridge_indexs = [168, 6, 197, 195]
nose_bridge_right_indexs = [193, 122, 196, 3]
nose_bridge_left_indexs = [417, 351, 419, 248]

nose_head_indexs = [5, 4, 1, 19, 94]
nose_head_right_indexs = [ 51, 45, 44, 125, 141]
nose_head_left_indexs = [ 281, 275, 274, 354, 370]


nose_right_index = 64
nose_left_index = 294
nose_end_index = 94
nose_end_middle_index = 19
nose_start_index = 168

# forehead
forehead_end_indexs = [107, 9, 136]
forehead_start_indexs = [109, 10, 338]

# chin
chin_end_index = 152
chin_end_right_indexs = [149, 176, 148]
chin_end_left_indexs = [378, 400, 377]

# jaw
jaw_right_indexs = [127, 234, 93, 132, 58, 172, 136, 150, 149]
jaw_left_indexs = [356, 454, 323, 361, 288, 397, 365, 379, 378]

# temple
temple_right_index = 127
temple_left_index = 356

# faceOval
faceOval_right_indexs = [148, 176, 149, 150, 136, 
                         172, 58, 132, 93, 234,
                         127, 162, 21, 54, 103, 
                         67, 109]

faceOval_left_indexs = [ 338, 297, 332, 284, 251, 
                         389, 356, 454, 323, 361, 
                         288, 397, 365, 379, 378, 
                         400, 377]
face_center_index = 1

def GetVectorLength(vector):
    return np.linalg.norm(vector)

def GetLength(point0, point1):
    return np.linalg.norm(point0 - point1)

def GetLengthBetweenPointLine(point, line_point0, line_point1):
    return np.linalg.norm(np.cross(line_point1 - line_point0, line_point0 - point)) / np.linalg.norm(line_point1 - line_point0)

def GetDegreeBetweenVectorXYPlane(vector):
    return np.arccos(vector[2] / np.linalg.norm(vector))

def GetMaxAngleIndex(points):
    max_angle = 0
    max_angle_index = 0
    # get dy/dx
    for i in range(1,len(points)-2):
        vec1 = points[i] - points[i-1]
        vec2 = points[i+1] - points[i]
        
        #get between angle
        angle = np.arccos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

        if angle > max_angle:
            max_angle = angle
            max_angle_index = i

    return max_angle_index

def GetProportion(point, standard_point0, standard_point1):
    foot_of_perpendicular = standard_point0 + np.dot(point - standard_point0, standard_point1 - standard_point0) / np.dot(standard_point1 - standard_point0, standard_point1 - standard_point0) * (standard_point1 - standard_point0)
    return GetLength(foot_of_perpendicular, standard_point0) / GetLength(standard_point0, standard_point1)

def GetSymmetry(points):
    right_points = points[faceOval_right_indexs]
    left_points = points[faceOval_left_indexs]
    right_center = np.mean(right_points, axis=0)
    left_center = np.mean(left_points, axis=0)
    symVect = 2*points[face_center_index] - right_center - left_center
    symVect = (0, symVect[1], symVect[2]) 
    return GetVectorLength(symVect)

def GetSkinColor(colors, n_clusters=3):
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(colors)
    labels = kmeans.labels_
    
    # Find the largest cluster
    largest_cluster_index = np.argmax(np.bincount(labels))
    
    # Extract the colors in the largest cluster
    largest_cluster_colors = colors[labels == largest_cluster_index]
    
    # Compute the median color of the largest cluster
    median_color = np.median(largest_cluster_colors, axis=0)
    
    return median_color

def GetLipColor(colors):
    # get lip indexs from mediapipe
    lip_indexes = top_lip_indexes + bottom_lip_indexes
    lip_colors = colors[lip_indexes]
    mean_color = np.mean(lip_colors, axis=0)    
    return mean_color

def GetEyeBetween(points):
    return GetLength(points[eye_front_left_index], points[eye_front_right_index])

def GetEyeLength(points):
    right_length = GetLength(points[eye_front_right_index], points[eye_back_right_index])
    left_length = GetLength(points[eye_front_left_index], points[eye_back_left_index])
    return right_length + left_length

def GetEyeFront(points):
    right_front_length = GetLengthBetweenPointLine(points[eye_front_right_index], points[eye_top_right_index], points[eye_bottom_right_index])
    left_front_length = GetLengthBetweenPointLine(points[eye_front_left_index], points[eye_top_left_index], points[eye_bottom_left_index])
    return right_front_length + left_front_length

def GetEyeBack(points):
    right_back_length = GetLengthBetweenPointLine(points[eye_back_right_index], points[eye_top_right_index], points[eye_bottom_right_index])
    left_back_length = GetLengthBetweenPointLine(points[eye_back_left_index], points[eye_top_left_index], points[eye_bottom_left_index])
    return right_back_length + left_back_length

def GetEyeAbove(points):
    right_above_length = 0
    left_above_length = 0
    for i in range(len(eye_above_right_indexes)):
        right_above_length += GetLengthBetweenPointLine(points[eye_above_right_indexes[i]], points[eye_front_right_index], points[eye_back_right_index])
        left_above_length += GetLengthBetweenPointLine(points[eye_above_left_indexes[i]], points[eye_front_left_index], points[eye_back_left_index])
    return right_above_length + left_above_length

def GetEyeBelow(points):
    right_below_length = 0
    left_below_length = 0
    for i in range(len(eye_below_right_indexes)):
        right_below_length += GetLengthBetweenPointLine(points[eye_below_right_indexes[i]], points[eye_front_right_index], points[eye_back_right_index])
        left_below_length += GetLengthBetweenPointLine(points[eye_below_left_indexes[i]], points[eye_front_left_index], points[eye_back_left_index])
    return right_below_length + left_below_length

def GetEyeDegree(points):
    right_eye = points[eye_front_right_index] - points[eye_back_right_index]
    right_eye = (0, right_eye[1], right_eye[2]) 

    left_eye = points[eye_front_left_index] - points[eye_back_left_index]
    left_eye = (0, left_eye[1], left_eye[2])
    
    right_eye_degree = GetDegreeBetweenVectorXYPlane(right_eye)
    left_eye_degree = GetDegreeBetweenVectorXYPlane(left_eye)

    if right_eye_degree < 0:
        print("right eye degree is negative" + right_eye)
    if left_eye_degree < 0:
        print("left eye degree is negative: " + left_eye)

    return right_eye_degree + left_eye_degree

def GetBrowBetween(points):
    right_brow = points[brow_start_right_indexs[0]] + points[brow_start_right_indexs[1]]
    left_brow = points[brow_start_left_indexs[0]] + points[brow_start_left_indexs[1]]
    return GetLength(right_brow, left_brow)

def GetBrowFront(points):
    right_fronts = points[brow_start_right_indexs[0]] + points[brow_start_right_indexs[1]]
    right_archs = points[brow_arch_right_indexs[0]] + points[brow_arch_right_indexs[1]]

    left_fronts = points[brow_start_left_indexs[0]] + points[brow_start_left_indexs[1]]
    left_archs = points[brow_arch_left_indexs[0]] + points[brow_arch_left_indexs[1]]

    return GetLength(right_fronts, right_archs) + GetLength(left_fronts, left_archs)

def GetBrowBack(points):
    right_backs = points[brow_end_right_indexs[0]] + points[brow_end_right_indexs[1]]
    right_archs = points[brow_arch_right_indexs[0]] + points[brow_arch_right_indexs[1]]

    left_backs = points[brow_end_left_indexs[0]] + points[brow_end_left_indexs[1]]
    left_archs = points[brow_arch_left_indexs[0]] + points[brow_arch_left_indexs[1]]

    return GetLength(right_backs, right_archs) + GetLength(left_backs, left_archs)

def GetBrowDegree(points):
    right_brow = points[brow_start_right_indexs[0]] - points[brow_end_right_indexs[0]]
    left_brow = points[brow_start_left_indexs[0]] - points[brow_end_left_indexs[0]]
    right_brow[0] = 0
    left_brow[0] = 0

    return GetDegreeBetweenVectorXYPlane(right_brow) + GetDegreeBetweenVectorXYPlane(left_brow)

def GetBrowThickness(points):
    right_fronts = GetLength(points[brow_start_right_indexs[0]], points[brow_start_right_indexs[1]])
    right_archs = GetLength(points[brow_arch_right_indexs[0]], points[brow_arch_right_indexs[1]])

    left_fronts = GetLength(points[brow_start_left_indexs[0]], points[brow_start_left_indexs[1]])
    left_archs = GetLength(points[brow_arch_left_indexs[0]], points[brow_arch_left_indexs[1]])

    return right_fronts + right_archs + left_fronts + left_archs

def GetBrowShape(points):
    right_arch = points[brow_arch_right_indexs[0]] + points[brow_arch_right_indexs[1]]
    right_start = points[brow_start_right_indexs[0]] + points[brow_start_right_indexs[1]]
    right_end = points[brow_end_right_indexs[0]] + points[brow_end_right_indexs[1]]

    left_arch = points[brow_arch_left_indexs[0]] + points[brow_arch_left_indexs[1]]
    left_start = points[brow_start_left_indexs[0]] + points[brow_start_left_indexs[1]]
    left_end = points[brow_end_left_indexs[0]] + points[brow_end_left_indexs[1]]

    right_shape = GetLengthBetweenPointLine(right_arch, right_start, right_end) / GetLength(right_start, right_end)
    left_shape = GetLengthBetweenPointLine(left_arch, left_start, left_end) / GetLength(left_start, left_end)

    return right_shape + left_shape

def GetNoseLength(points):
    nose_start = points[nose_start_index]
    nose_end = points[nose_end_middle_index]

    return GetLength(nose_end, nose_start)

def GetNoseBridgeThickness(points):
    nose_bridge_right = points[nose_bridge_indexs] - points[nose_bridge_right_indexs]
    nose_bridge_left = points[nose_bridge_indexs] - points[nose_bridge_left_indexs]

    nose_bridge_right = nose_bridge_right.mean(axis=0)
    nose_bridge_left = nose_bridge_left.mean(axis=0)
    return abs(nose_bridge_right[1]) + abs(nose_bridge_left[1])

def GetNoseHeadThickness(points):
    nose_head_right = points[nose_head_indexs] - points[nose_head_right_indexs]
    nose_head_left = points[nose_head_indexs] - points[nose_head_left_indexs]
    nose_head_right = nose_head_right.mean(axis=0)
    nose_head_left = nose_head_left.mean(axis=0)
    return abs(nose_head_right[1]) + abs(nose_head_left[1])

def GetNoseEndSharpness(points):

    nose_end = points[nose_end_index] - points[nose_bridge_indexs[-1]]
    return GetVectorLength(nose_end)

def GetNoseAlar(points):
    nose_right = points[nose_right_index] - points[nose_bridge_indexs[-1]]
    nose_left = points[nose_left_index] - points[nose_bridge_indexs[-1]]
    return GetVectorLength(nose_right) + GetVectorLength(nose_left)

def GetPhiltrum(points):
    philtrum = points[nose_end_index] - points[top_lip_top_index]
    return GetVectorLength(philtrum)

def GetLipLength(points):    
    return GetVectorLength(points[lip_right_end_index] - points[lip_left_end_index])

def GetUpperLipThickness(points):
    return GetVectorLength(points[top_lip_top_index] - points[top_lip_bottom_index])

def GetLowerLipThickness(points):
    return GetVectorLength(points[bottom_lip_top_index] - points[bottom_lip_bottom_index])

def GetForeheadLength(points):
    forehead_vector = points[forehead_start_indexs] - points[forehead_end_indexs]
    return GetVectorLength(forehead_vector)

def GetChinLength(points):
    return GetVectorLength(points[bottom_lip_bottom_index] - points[chin_end_index])

def GetChinWidth(points):
    right_jaw = points[jaw_right_indexs[2]] - points[chin_end_index]
    left_jaw = points[jaw_left_indexs[2]] - points[chin_end_index]
    return abs(right_jaw[1]) + abs(left_jaw[1])

def GetJawPointsIndex(points):
    right_jaw_points = points[jaw_right_indexs]
    right_jaw_points = right_jaw_points[:,1:]
    right_jaw_point_index = GetMaxAngleIndex(right_jaw_points)
    right_jaw_point_index = jaw_right_indexs[right_jaw_point_index]

    left_jaw_points = points[jaw_left_indexs]
    left_jaw_points = left_jaw_points[:,1:]
    left_jaw_point_index = GetMaxAngleIndex(left_jaw_points)
    left_jaw_point_index = jaw_left_indexs[left_jaw_point_index]

    return right_jaw_point_index, left_jaw_point_index


def GetJawWide(points):
    
    chin = points[jaw_right_indexs[0]][1:]
    temple = points[jaw_right_indexs[-1]][1:]

    right_jaw_point_index, left_jaw_point_index = GetJawPointsIndex(points)

    jaw = points[right_jaw_point_index][1:]
    right_jaw = GetLengthBetweenPointLine(jaw, chin, temple)


    chin = points[jaw_left_indexs[0]][1:]
    temple = points[jaw_left_indexs[-1]][1:]

    jaw = points[left_jaw_point_index][1:]
    left_jaw = GetLengthBetweenPointLine(jaw, chin, temple)

    return right_jaw + left_jaw

def GetJawPosition(points):
    right_jaw_point_index, left_jaw_point_index = GetJawPointsIndex(points)

    right_jaw = points[right_jaw_point_index][1:]
    right_temple = points[jaw_right_indexs[0]][1:]
    chin = points[jaw_right_indexs[-1]][1:]
    right_proportion = GetProportion(right_jaw, chin, right_temple)

    left_jaw = points[left_jaw_point_index][1:]
    left_temple = points[jaw_left_indexs[0]][1:]
    chin = points[jaw_left_indexs[-1]][1:]
    left_proportion = GetProportion(left_jaw, chin, left_temple)

    return right_proportion + left_proportion

def ExtractFeatures(points, colors):
    dict = {}
    
    # filter out the outliers
    symmetry = GetSymmetry(points)
    if symmetry > 0.1:
        print("out of Symeetry: " + f'{symmetry}')
        return None

    # dict.update({"symmetry": symmetry})
    # dict.update({"eyeBetween": GetEyeBetween(points)})
    # dict.update({"eyeFront": GetEyeFront(points)})
    # dict.update({"eyeBack": GetEyeBack(points)})
    # dict.update({"eyeLength": GetEyeLength(points)})
    # dict.update({"eyeAbove": GetEyeAbove(points)})
    # dict.update({"eyeBelow": GetEyeBelow(points)})
    # dict.update({"eyeDegree": GetEyeDegree(points)})

    # dict.update({"browBetween": GetBrowBetween(points)})
    # dict.update({"browFront": GetBrowFront(points)})
    # dict.update({"browBack": GetBrowBack(points)})
    # dict.update({"browDegree": GetBrowDegree(points)})
    # dict.update({"browThickness": GetBrowThickness(points)})
    # dict.update({"browShape": GetBrowShape(points)})

    dict.update({"noseLength": GetNoseLength(points)})
    dict.update({"noseBridgeThickness": GetNoseBridgeThickness(points)})
    dict.update({"noseHeadThickness": GetNoseHeadThickness(points)})
    # dict.update({"noseAlar": GetNoseAlar(points)})
    # dict.update({"philtrum": GetPhiltrum(points)})

    # dict.update({"lipLength": GetLipLength(points)})
    # dict.update({"upperLipThickness": GetUpperLipThickness(points)})
    # dict.update({"lowerLipThickness": GetLowerLipThickness(points)})

    # dict.update({"foreheadLength": GetForeheadLength(points)})

    # dict.update({"chinLength": GetChinLength(points)})
    # dict.update({"chinWidth": GetChinWidth(points)})

    # dict.update({"jawWide": GetJawWide(points)})
    # dict.update({"jawPosition": GetJawPosition(points)})

    # dict.update({"skinColor": GetSkinColor(colors)})
    # dict.update({"lipColor": GetLipColor(colors)})
    return dict

def printFeatures(dicts):
    for key in dicts:
        print(f'{key}: {dicts[key]}')

def SaveValues(points_path, export_path):
    try:
        data = np.load(points_path, allow_pickle=True)
        points = data[0][0]
        colors = data[1][0]

        values = ExtractFeatures(points, colors)
        if values is None:
            return

        if not os.path.exists(export_path):
            os.makedirs(export_path)

        export_file_path = f'{export_path}/{points_path.split("/")[-1].split(".")[0]}.pickle'
        with open(export_file_path, 'wb') as handle:
            pickle.dump(values, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(f'{export_file_path} saved')
    except Exception as e:
        print(f'An error occurred: {e}')


def SaveBatchValues(path, export_path):
    for file in os.listdir(path):
        if file.endswith('.npy'):
            SaveValues(f'{path}/{file}', export_path)
