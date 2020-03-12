""" Rendering to image and video. """

import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2

# from operator import itemgetter

from Obj import serialize, SIZE

DPI = 300

def render(nodes, tetras, force=None, shape='CUBE', filename='x.png'):
    # npnodes = np.array(nodes)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d(-SIZE, SIZE*2)
    ax.set_ylim3d(-SIZE, SIZE*2)
    ax.set_zlim3d(-SIZE, SIZE*2)

    # Render nodes as dot cloud
    # xs = list(map(itemgetter(0), nodes))
    # ys = list(map(itemgetter(1), nodes))
    # zs = list(map(itemgetter(2), nodes))
    # xs = np.squeeze(npnodes[:, 0])
    # ys = np.squeeze(npnodes[:, 1])
    # zs = np.squeeze(npnodes[:, 2])
    xs = [ n[0] for n in nodes ]
    ys = [ n[1] for n in nodes ]
    zs = [ n[2] for n in nodes ]
    ax.scatter(xs=xs, ys=ys, zs=zs, s=1, color='cyan')
    

    # xs = np.squeeze(npnodes[:, 0])
    # ys = np.squeeze(npnodes[:, 1])
    # zs = np.squeeze(npnodes[:, 2])
    # for x in range(SIZE+1):
    #     index = serialize(x,0,0)
    #     xs.append(nodes[index][0])
    #     ys.append(nodes[index][1])
    
    # Render edges
    if shape == 'CUBE':
        S = SIZE
        edge00i = [ nodes[ serialize(0,0,i) ] for i in range(SIZE+1) ]
        edge01i = [ nodes[ serialize(0,S,i) ] for i in range(SIZE+1) ]
        edge10i = [ nodes[ serialize(S,0,i) ] for i in range(SIZE+1) ]
        edge11i = [ nodes[ serialize(S,S,i) ] for i in range(SIZE+1) ]
        edge0i0 = [ nodes[ serialize(0,i,0) ] for i in range(SIZE+1) ]
        edge0i1 = [ nodes[ serialize(0,i,S) ] for i in range(SIZE+1) ]
        edge1i0 = [ nodes[ serialize(S,i,0) ] for i in range(SIZE+1) ]
        edge1i1 = [ nodes[ serialize(S,i,S) ] for i in range(SIZE+1) ]
        edgei00 = [ nodes[ serialize(i,0,0) ] for i in range(SIZE+1) ]
        edgei01 = [ nodes[ serialize(i,0,S) ] for i in range(SIZE+1) ]
        edgei10 = [ nodes[ serialize(i,S,0) ] for i in range(SIZE+1) ]
        edgei11 = [ nodes[ serialize(i,S,S) ] for i in range(SIZE+1) ]
        for edge in [ edge00i, edge01i, edge10i, edge11i, edge0i0, edge0i1, edge1i0, edge1i1, edgei00, edgei01, edgei10, edgei11]:
            xs = [ n[0] for n in edge ]
            ys = [ n[1] for n in edge ]
            zs = [ n[2] for n in edge ]
            ax.plot(xs, ys, zs, color='blue')
    if shape == 'SINGLE':
        for node_index in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]:
            xs = [nodes[node_index[0]][0], nodes[node_index[1]][0]]
            ys = [nodes[node_index[0]][1], nodes[node_index[1]][1]]
            zs = [nodes[node_index[0]][2], nodes[node_index[1]][2]]
            ax.plot(xs, ys, zs, color='blue')

    # Render force
    if force is not None:
        xs = [ n[0] for n in nodes ]
        ys = [ n[1] for n in nodes ]
        zs = [ n[2] for n in nodes ]
        us = [ f[0] for f in force ]
        vs = [ f[1] for f in force ]
        ws = [ f[2] for f in force ]
        ax.quiver(xs, ys, zs, us, vs, ws)


    if filename[-4:] != '.png':
        filename += '.png'
    plt.savefig(filename, dpi=DPI)
    
    plt.close(fig)
    return filename



def make_video(filenames):
    video_name = os.path.join('out', 'out.avi')
    img_array = []
    for filename in filenames:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
    
    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 8, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
