import os
from Obj import load_obj, load_single, deform, verify_volume
from Render import render, make_video
from Formula import *


# Time configurations
# 
# in the simulation world, simulate a period of 1000 seconds
DURATION = 1200
# in the simulation world, upgrade the object state every 1 second
DELTA_TIME = 1
# in the real world (output video), time is 10 times as fast as the simulation world
PLAYBACK_RATE = 120
# in the real world (output video), the object is rendered 25 times every second (frames per second)
FPS = 25


if __name__ == "__main__":
    
    # 1. Load Object
    # X: array[][coord, 3]
    #     Configuration(position of nodes). Each element correseponds to a node, and is a 3-element array that stores the node's position.
    # T: array[][node#, 4]
    #     Tetrahedral mesh. Each element correspond to a tetrahedral, and is a 4-element array that stores the INDEX of the nodes (in X) of the tetrahedral.
    X, T = load_obj()
    print(len(X), " nodes.")
    print(len(T), " tetrahedrals.")
    
    # 2. Precomputation and initialization
    B, W = precompute(X, T)
    X = deform(X)
    # Initialize velocities to 0
    V = np.zeros((len(X), 3))

    # 3. Main update loop
    now = 0 # current time
    frame_counter = 0 # number of frames rendered
    rendered_images = [] # filenames of rendered images
    while now < DURATION:

        # Update config (X) and new velocities (V)
        # return F for debugging
        F = update_XV(X, T, V, B, W, DELTA_TIME)
        
        # Render to image file
        video_sample_time = frame_counter / FPS * PLAYBACK_RATE # the time (in the simulation world) from which next frame is rendered
        if now >= video_sample_time:
            print("Rendering frame", frame_counter, "/", int(DURATION / DELTA_TIME / PLAYBACK_RATE * FPS))
            filename = os.path.join("out", str(frame_counter)+".png")
            render(X, T, filename=filename)
            rendered_images.append(filename)
            frame_counter += 1

        now += DELTA_TIME

    print("Generating video...")
    make_video(rendered_images, os.path.join("out", "out.avi"), FPS)
