""" Rendering to image and video. """

import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
from Object import serialize, SIZE


DPI = 300


def render(nodes, tetras, force=None, filename="out_default.png"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim3d(-0.4*SIZE, 1.4*SIZE)
    ax.set_ylim3d(-0.4*SIZE, 1.4*SIZE)
    ax.set_zlim3d(0        , 1.4*SIZE)

    # Render nodes as dot cloud
    xs = [ n[0] for n in nodes ]
    ys = [ n[1] for n in nodes ]
    zs = [ n[2] for n in nodes ]
    ax.scatter(xs=xs, ys=ys, zs=zs, s=1, color="turquoise", alpha=0.5)
    
    # Render edges
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
    for edge in [ edge00i, edge01i, edge10i, edge11i, edge0i0, edge0i1, edge1i0, edge1i1, edgei00, edgei01, edgei10, edgei11 ]:
        xs = [ n[0] for n in edge ]
        ys = [ n[1] for n in edge ]
        zs = [ n[2] for n in edge ]
        ax.plot(xs, ys, zs, color="dodgerblue")

    # Render force
    if force is not None:
        xs = [ n[0] for n in nodes ]
        ys = [ n[1] for n in nodes ]
        zs = [ n[2] for n in nodes ]
        us = [ f[0] for f in force ]
        vs = [ f[1] for f in force ]
        ws = [ f[2] for f in force ]
        ax.quiver(xs, ys, zs, us, vs, ws)

    if filename[-4:] != ".png":
        filename += ".png"
    plt.savefig(filename, dpi=DPI)
    plt.close(fig)


def make_video(images, video_filename, FPS):

    # Configure video writer ("out") based on the first image
    height, width, _ = cv2.imread(images[0]).shape
    out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*"DIVX"), FPS, (width, height))
    
    # Write images
    for image in images:
        out.write(cv2.imread(image))
    out.release()
