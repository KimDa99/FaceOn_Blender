import os
import numpy as np

def rotation_matrix(axis, theta):
    axis = axis / np.linalg.norm(axis)
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])

def normalizePoints(points):
    foreHead_point = points[10]
    chin_point = points[152]

    left_eye_point = points[263]
    right_eye_point = points[33]

    # make points 152 origin (0,0,0)
    points -= points[152]

    p_norm = points[10] / np.linalg.norm(points[10])

    z_axis = np.array([0, 0, 1])
    rotation_axis = np.cross(p_norm, z_axis)
    rotation_axis_norm = rotation_axis / np.linalg.norm(rotation_axis)

    angle = np.arccos(np.dot(p_norm, z_axis))
    R = rotation_matrix(rotation_axis_norm, angle)
    points = points @ R.T

    nose_point = np.array([points[1][0], points[1][1], 0])
    n_norm = nose_point / np.linalg.norm(nose_point)

    x_axis = np.array([1, 0, 0])
    rotation_axis = np.cross(n_norm, x_axis)
    rotation_axis_norm = rotation_axis / np.linalg.norm(rotation_axis)

    angle = np.arccos(np.dot(n_norm, x_axis))

    # Compute the rotation matrix
    R = rotation_matrix(rotation_axis_norm, angle)
    points = points @ R.T

    # normalize the points to fit in the screen
    points[:, 0] -= np.min(points[:, 0])
    points[:, 1] -= np.min(points[:, 1])
    points[:, 2] -= np.min(points[:, 2])

    scaling_factor = np.max(points[:, 1])
    points[:, 0] /= scaling_factor
    points[:, 1] /= scaling_factor
    points[:, 2] /= scaling_factor

    return points

def GetNormalizedPoints(npArray_file_path):
    points = np.load(npArray_file_path)
    return normalizePoints(points)

def SaveNormalizedPoints(npArray_file_path, target_path):
    points = GetNormalizedPoints(npArray_file_path)

    if not os.path.exists(target_path):
        os.makedirs(target_path)
    base_filename = npArray_file_path.split('/')[-1]
    base_filename = base_filename[:base_filename.rfind('.')]
    np.save(f'{target_path}/{base_filename}.npy', points)

def SaveNormalizedBatch(npArray_file_paths, target_path):
    for file in os.listdir(npArray_file_paths):
        if file.endswith('.npy'):
            if file.endswith('_color.npy'):
                continue
            SaveNormalizedPoints(f'{npArray_file_paths}/{file}', target_path)
