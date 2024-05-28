import os
import numpy as np

path = 'FaceOn/data/combined_Normalized/part1'

points = []
colors = []
for file in os.listdir(path):
    if file.endswith('.npy'):
        data = np.load(f'{path}/{file}')
        points.append(data[0][0])
        colors.append(data[1][0])

points = np.array(points)
colors = np.array(colors)

# get the mean of the points and colors
mean_points = np.mean(points, axis=0)
mean_colors = np.mean(colors, axis=0)

# save the mean points and colors
np.save('FaceOn/data/mean_points.npy', mean_points)
np.save('FaceOn/data/mean_colors.npy', mean_colors)
