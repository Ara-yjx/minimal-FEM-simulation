""" Rendering to image and video. """

import os
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# from operator import itemgetter

from Obj import serialize, SIZE

DPI = 300
BITRATE = 1800
FPS = 18

# Singleton pattern for plot and data
result_data = []
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d(-0.4*SIZE, 1.4*SIZE)
ax.set_ylim3d(-0.4*SIZE, 1.4*SIZE)
ax.set_zlim3d(0, 1.4*SIZE)

node_plot = ax.scatter(xs=[], ys=[], zs=[], s=1, color='turquoise', alpha=0.5)


def render_frame(frame_index):

    # plt.cla()
    ax.clear()


    nodes = result_data[frame_index]["nodes"]
    forces = result_data[frame_index]["forces"]

    node_x = [ n[0] for n in nodes ]
    node_y = [ n[1] for n in nodes ]
    node_z = [ n[2] for n in nodes ]
    # node_plot = ax.scatter(xs=node_x, ys=node_y, zs=node_z, s=1, color='turquoise', alpha=0.5)
    # print(node_plot)
    
    node_plot.set_data((node_x, node_y))
    node_plot.set_3d_properties(node_z)

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
        edge_x = [ n[0] for n in edge ]
        edge_y = [ n[1] for n in edge ]
        edge_z = [ n[2] for n in edge ]
        ax.plot(edge_x, edge_y, edge_z, color='dodgerblue')

    # Render force
    if forces is not None:
        us = [ f[0] for f in forces ]
        vs = [ f[1] for f in forces ]
        ws = [ f[2] for f in forces ]
        ax.quiver(node_x, node_y, node_z, us, vs, ws)
    
    return ax


def render(result):
    global result_data
    result_data = result
    anim = animation.FuncAnimation(fig, render_frame, frames=len(result_data), blit=True)
    from matplotlib.animation import FFMpegWriter
    writer = FFMpegWriter(fps=FPS, codec="mpeg4", bitrate=BITRATE) # choose mpeg4 encoder for maximum compatibility
    anim.save("test.mp4", writer=writer, dpi=DPI)



# def test_render():


# if __name__ == "__main__":
#     test_render()


