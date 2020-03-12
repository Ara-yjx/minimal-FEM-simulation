import os
from Obj import load_obj, load_single, deform, verify_volume
from Render import render, make_video
from Formula import *


N_STEPS = 25 # number of time steps

if __name__ == "__main__":

    # ref_xs, def_xs: array[][coord, 3]
    #     ref_xs: Reference(undeformed) configuration. Each element correseponds to a node, and is a 3-element array that stores the node's position.
    #     def_xs: Deformed configuration. Same structure.
    # tetras: array[][node#, 4]
    #     tetras: Tetrahedral mesh. Each element correspond to a tetrahedral, and is a 4-element array that stores the INDEX of the nodes (in X) of the tetrahedral.
    ref_X, Tetras, shape = load_single()
    print(len(ref_X), " nodes.")
    print(len(Tetras), " tetrahedrals.")
    # verify_volume(ref_X, Tetras) # for debug

    def_X = deform(ref_X)
    # render(ref_X, Tetras, shape=shape, filename='ref')
    # render(def_X, Tetras, shape=shape, filename='def')

    B, W = precompute(ref_X, Tetras)
    
    # Initialize velocities to 0
    V = [[0,0,0]] * len(ref_X)

    filenames = []

    for step in range(N_STEPS):
        print('Rendering ', step, '/', N_STEPS)

        # Update config (X) and new velocities (V)
        # return F for debugging
        F = update_XV(def_X, Tetras, V, B, W)

        filename = render(def_X, Tetras, F, shape, os.path.join('out', str(step)))

        filenames.append(filename)

    make_video(filenames)


    
    



