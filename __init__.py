import os
from Obj import load_obj, load_single, deform, verify_volume
from Render import render
from Formula import *


# N_STEPS = 20 # number of time steps
# STEP_PER_FRAME = 10

# in the simulation world, simulate a period of 1000 seconds
DURATION = 100
# in the simulation world, upgrade the object state every 1 second
REFRESH_INTERVAL = 1
# in the real world (output video), time is 10 times as fast as the simulation world
PLAYBACK_RATE = 100
# in the real world (output video), the object is rendered 20 times every second (frames per second)
FPS = 20


if __name__ == "__main__":

    result = []
    # ref_X: array[][3]
    #     ref_xs: Reference(undeformed) configuration. Each element correseponds to a node, and is a 3-element array that stores the node's position.
    #     def_xs: Deformed configuration. Same structure.
    # tetras: array[][4]
    #     tetras: Tetrahedral mesh. Each element correspond to a tetrahedral, and is a 4-element array that stores the INDEX of the nodes (in X) of the tetrahedral.
    ref_X, Tetras, shape = load_obj()
    print(len(ref_X), "nodes.")
    print(len(Tetras), "tetrahedrals.")
    # verify_volume(ref_X, Tetras) # for debug

    def_X = deform(ref_X)

    B, W = precompute(ref_X, Tetras)
    
    # Initialize velocities to 0
    # V = [[0,0,0]] * len(ref_X)
    V = np.zeros((len(ref_X), 3))

    filenames = []

    now = 0.0 # current time
    frame_counter = 0
    while now < DURATION:

        # Update config (X) and new velocities (V)
        # return F for debugging
        F = update_XV(def_X, Tetras, V, B, W)

        video_sample_time = frame_counter / FPS * PLAYBACK_RATE # the time (in simulation world) from which next frame is rendered
        if video_sample_time <= now:
            result.append({"nodes": def_X, "forces": F})
            if (frame_counter + 1) // FPS > frame_counter // FPS:
                print((frame_counter + 1) // FPS, '/', DURATION / PLAYBACK_RATE, 'seconds rendered')
            frame_counter += 1

        now += REFRESH_INTERVAL

    print('Rendering to video...')
    render(result[:1])


    
    



