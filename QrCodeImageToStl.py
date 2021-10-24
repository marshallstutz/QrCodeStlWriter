from PIL import Image
import numpy as np
import time
import pygame
import math
from stl import mesh
import stl
image = Image.open("frame.png")
pixelLocations = []
def drawRect():
    pygame.init()
    surface = pygame.display.set_mode((1200,1200))
    surface.fill((255,255,255))
    color = (0,0,0)
    for rect in pixelLocations:
        pygame.draw.rect(surface, color, 
        pygame.Rect((rect[1]-rect[2]/2)*4, (rect[0]-rect[3]/2)*4, (rect[2])*4, (rect[3])*4))
        pygame.display.flip()
    while True:
        time.sleep(1)

def combined_stl(meshes, save_path="./combined.stl"):
    combined = mesh.Mesh(np.concatenate([m.data for m in meshes]))
    combined.save(save_path, mode=stl.Mode.ASCII)

def roundup(x, len):
    return int(math.ceil(x / float(len))) * len

def normalizeRects():
    i = 0 
    while True:
    #for i in range(0, len(pixelLocations)):
        if i > len(pixelLocations)-1:
            break
        if pixelLocations[i][2] < 3 or pixelLocations[i][3] < 3:
            pixelLocations.pop(i)
        else:
            i = i + 1
    sideLen = min(pixelLocations[0][2], pixelLocations[0][3])
    for rect in pixelLocations:
            rect[2] = roundup(rect[2], sideLen)
            rect[3] = roundup(rect[3], sideLen)
        

image_sequence = image.getdata()
image_array = np.array(image_sequence)
#print(image_array)
#print(len(image_array))
length = int(np.sqrt(len(image_array)))
#print(length)
print(image_array.size)
arr = np.reshape(image_array, (-1, length, 4))

countBlack = 0
countWhite = 0
for a in range(0,len(arr)):
    for b in range(0, len(arr[a])):
        if arr[a][b][0] < 123:
            countBlack = countBlack + 1
            pixelLocations.append([float(a),float(b),1,1])
#print(countWhite)
#print(countBlack)
#print(pixelLocations)

#loop through y values where x is constant and combine if next value is also black
i = 0
pixelLocations.sort()
#print(pixelLocations)
#exit()
while True:
#for i in range(0, len(pixelLocations)-1):
    if i == len(pixelLocations)-1:
        break
    if pixelLocations[i][0] == pixelLocations[i+1][0] and pixelLocations[i][1] + pixelLocations[i][2]/2 == pixelLocations[i+1][1] - pixelLocations[i+1][2]/2:
        pixelLocations[i][1] = (((pixelLocations[i][1] - pixelLocations[i][2]/2) + (pixelLocations[i+1][1] + pixelLocations[i+1][2]/2))/2)
        pixelLocations[i][2] = pixelLocations[i+1][2] + pixelLocations[i][2]
        pixelLocations.pop(i+1)
    else:
        i = i + 1
#drawRect()
pixelLocations.sort(key=lambda x:x[1],reverse=False)
#print(pixelLocations)
#print(len(pixelLocations))
i = 0
while True:
#for i in range(0, len(pixelLocations)-1):
    if i == len(pixelLocations)-1:
        break
    if pixelLocations[i][1] == pixelLocations[i+1][1] and pixelLocations[i][2] == pixelLocations[i+1][2] and pixelLocations[i][0] + pixelLocations[i][3]/2 == pixelLocations[i+1][0] - pixelLocations[i+1][3]/2:
        pixelLocations[i][0] = (((pixelLocations[i][0] - pixelLocations[i][3]/2) + (pixelLocations[i+1][0] + pixelLocations[i+1][3]/2))/2)
        pixelLocations[i][3] = pixelLocations[i+1][3] + pixelLocations[i][3]
        pixelLocations.pop(i+1)
    else:
        i = i + 1
#print(pixelLocations)
pixelLocations.sort(key=lambda x:x[0],reverse=False)
#print(pixelLocations)
normalizeRects()
print(pixelLocations)
#drawRect()
cubes = []
for rect in pixelLocations:
# Define the 8 vertices of the cube
#pygame.Rect(rect[1]-rect[2]/2, rect[0]-rect[3]/2, rect[2], rect[3]))
    left = rect[1]-rect[2]/2
    right = rect[1]+rect[2]/2
    top = rect[0]-rect[3]/2
    bottom = rect[0]+rect[3]/2
    posZ = 2
    negZ = 1
    vertices = np.array([\
        [left, top, negZ],
        [right, top, negZ],
        [right, bottom, negZ],
        [left, bottom, negZ],
        [left, top, posZ],
        [right, top, posZ],
        [right, bottom, posZ],
        [left, bottom, posZ]])
    # Define the 12 triangles composing the cube
    faces = np.array([\
        [0,3,1],
        [1,3,2],
        [0,4,7],
        [0,7,3],
        [4,5,6],
        [4,6,7],
        [5,1,2],
        [5,2,6],
        [2,3,6],
        [3,7,6],
        [0,1,5],
        [0,5,4]])

    # Create the mesh
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]
    cubes.append(cube)

vertices = np.array([\
    [0, 0, 0],
    [length, 0, 0],
    [length, length, 0],
    [0, length, 0],
    [0, 0, 1],
    [length, 0, 1],
    [length, length, 1],
    [0, length, 1]])
# Define the 12 triangles composing the cube
faces = np.array([\
    [0,3,1],
    [1,3,2],
    [0,4,7],
    [0,7,3],
    [4,5,6],
    [4,6,7],
    [5,1,2],
    [5,2,6],
    [2,3,6],
    [3,7,6],
    [0,1,5],
    [0,5,4]])

# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j],:]
cubes.append(cube)
combined_stl(cubes)
drawRect()
# Write the mesh to file "cube.stl"
#cube.save('qrcode.stl')