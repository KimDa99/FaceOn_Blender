import os
import cv2 as cv
import mediapipe as mp
import numpy as np

image_path0 = 'FaceOn/data/part1'
image_path1 = 'FaceOn/data/part2'
image_path2 = 'FaceOn/data/part3'

target_path = 'FaceOn/data/landmarks'

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.8)

def GetPointsColor(imagePath):
    try:
        image = cv.imread(imagePath)
        if image is None:
            print(f'Error: Unable to read image {imagePath}')
            return None, None

        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        if not results.multi_face_landmarks:
            print(f'Error: No face detected in {imagePath}')
            return None, None 

        landmarks = results.multi_face_landmarks[0].landmark
        points = np.array([(lm.x, lm.y, lm.z) for lm in landmarks])

        height, width, _ = image.shape
        points_2d = np.array([(int(lm.x * width), int(lm.y * height)) for lm in landmarks])
        colors = np.array([image[y, x] / 255.0 for x, y in points_2d])

        return points, colors
    except Exception as e:
        print(f'Error processing {imagePath}: {e}')
        return None, None

def SavePointsColor(imagePath, targetPath):
    try:
        point, color = GetPointsColor(imagePath)
        if point is None or color is None:
            return

        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        base_filename = os.path.basename(imagePath)
        base_filename = base_filename[:base_filename.rfind('.')]
        np.save(f'{targetPath}/{base_filename}.npy', point)
        np.save(f'{targetPath}/{base_filename}_color.npy', color)
        print(f'{targetPath}/{base_filename} saved')
    except Exception as e:
        print(f'Error saving {imagePath}: {e}')

# Get the points and colors for each image in all files
def process_images(image_path, target_path):
    print(f'Processing {image_path}')
    for image in os.listdir(image_path):
        image_path_full = os.path.join(image_path, image)
        SavePointsColor(image_path_full, target_path)

process_images(image_path0, f'{target_path}/part1')
process_images(image_path1, f'{target_path}/part2')
process_images(image_path2, f'{target_path}/part3')
