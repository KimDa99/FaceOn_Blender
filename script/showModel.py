import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

import os

def LoadTriangles(triangles_path='FaceOn/data/face_mesh_triangles.npy'):
    if os.path.exists(triangles_path):
        print("Loading triangles from existing file...")
        triangles = np.load(triangles_path)

    return triangles

def GetPointsColors(points_file, colors_file):
    points = np.load(points_file)
    colors = np.load(colors_file)
    return points, colors

def CreateAnimation(points, colors, triangles, name):
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
    ani = FuncAnimation(fig, update, frames=np.arange(0, 90, 1), interval=50)

    print("Saving the video...")
    # Save the animation as a video
    video_path = 'FaceOn/data/3d_Animated/' + str(name)+ '.mp4'
    ani.save(video_path, writer='ffmpeg')
    
# print('Starting')
# triangles = LoadTriangles()
# print('Triangles are loaded')
# points = np.load('FaceOn/data/means/total_mean_points.npy')
# colors = np.load('FaceOn/data/means/total_mean_colors.npy')
# print('points:', points)
# print('colors:', colors)
# CreateAnimation(points, colors, triangles, 'total_mean')
# print('Done')

def CreateBatchAnimation(triangles_path='FaceOn/data/face_mesh_triangles.npy', points_path='FaceOn/data/means', save_path='FaceOn/data/3d_Animated'):
    triangles = LoadTriangles(triangles_path)
    colors = np.load('FaceOn/data/means/total_mean_colors.npy')
    for file in os.listdir(points_path):
        if file.endswith('_points.npy'):
            points = np.load(f'{points_path}/{file}')
            print('points:', points)

            name = file.split('_')
            name = name[0] + '_' + name[1]
            print('creating animation for:', name)
            CreateAnimation(points, colors, triangles, name)
            print('Done')

CreateBatchAnimation(points_path='FaceOn/data/xyzNormalized/means_points_colors', save_path='FaceOn/data/xyzNormalized/3d_Animated')
