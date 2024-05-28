import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

import os

# Define the path for saving the triangles
output_file = 'FaceOn/data/face_mesh_triangles.npy'
points_file = 'FaceOn/data/combined_Normalized/part1/6_1_3_20170109141816261_combined.npy'
points = np.load(points_file)[0][0]
colors = np.load(points_file)[1][0]
# points = np.load('FaceOn\data\mean_points.npy')
# colors = np.load('FaceOn\data\mean_colors.npy')


print("Points shape: ", points.shape)
print(points)
print("colors shape: ", colors.shape)
print(colors)

# Check if the output file exists
if os.path.exists(output_file):
    print("Loading triangles from existing file...")
    triangles = np.load(output_file)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

print("Making Poly3DCollection...")
# Plot the polygons
polygons = []
for tri in triangles:
    pts = points[tri]
    poly = Poly3DCollection([pts])
    color = np.mean(colors[tri], axis=0)
    poly.set_facecolor(color)
    polygons.append(poly)
    ax.add_collection3d(poly)
print("Saving the polygons...")

# Function to update the plot for each frame
def update(frame):
    ax.view_init(elev=10., azim=frame)
    return polygons,

# Set the limits and labels for better visualization
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

# Ensure the aspect ratio is equal
ax.set_box_aspect([1,1,1])  # Aspect ratio is 1:1:1

print("Creating the animation...")
# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 1), interval=50)

print("Saving the video...")
# Save the animation as a video
video_path = 'FaceOn/data/3d_Animated' + points_file[points_file.rfind('/'):-4] + '.mp4'
ani.save(video_path, writer='ffmpeg')

plt.show()
