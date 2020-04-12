""" Object loading/creation and initial deformation. """

import numpy as np

SIZE = 10

def serialize(x, y, z):
    """ Given the position (x,y,z) of a node, 
        return its index in the nodes array. """
    return x*(SIZE+1)**2 + y*(SIZE+1) + z # fuck. power is **, not ^


def load_object():
    """ Create a cube object with edge length of SIZE. 
        Each 1*1*1 cube are divided into 5 tetrahedrals.
        Thus (SIZE+1)^3 nodes and 5*SIZE^3 tetrahedrals in total. """
    nodes = []
    tetras = []
    for ix in range(SIZE+1):
        for iy in range(SIZE+1):
            for iz in range(SIZE+1):
                nodes.append([ix, iy, iz])
    
    for ix in range(SIZE):
        for iy in range(SIZE):
            for iz in range(SIZE):
                node000 = serialize(ix, iy, iz) 
                node001 = serialize(ix, iy, iz+1) 
                node010 = serialize(ix, iy+1, iz) 
                node011 = serialize(ix, iy+1, iz+1) 
                node100 = serialize(ix+1, iy, iz) 
                node101 = serialize(ix+1, iy, iz+1) 
                node110 = serialize(ix+1, iy+1, iz) 
                node111 = serialize(ix+1, iy+1, iz+1)
                # bot(**0) and top(**1) divide on 000-110 and 011-101
                tetras.append([node000, node110, node100, node101]) #divide1, divide2, non-divide, top of non-divide
                tetras.append([node000, node110, node010, node011])
                tetras.append([node011, node101, node001, node000])
                tetras.append([node011, node101, node111, node110])
                tetras.append([node000, node110, node011, node101])

                #       011 ----------- 111
                #         / \         /|
                #        /   \       / |
                #       /     \     /  |
                #      /       \   /   |
                #     /         \ /    |
                # 001 ----------101\_  |
                #    |          /|   \_ 110
                #    |        /  |    / 
                #    |      /    |   /   
                #    |    /      |  /    
                #    |  /        | /    
                #    |/          |/     
                # 000 -----------100  

    return np.array(nodes), np.array(tetras)


class Deform:

    def stretch_z(nodes, extent=0.2):
        """ Stretch +z direction by <extent> """
        return np.array([ (n[0], n[1], n[2]*(1+extent)) for n in nodes])
        
    def translate_z(nodes, extent=0.2):        
        """ Move +z direction by <extent> """
        return np.array([ (n[0], n[1], n[2] + SIZE*extent) for n in nodes ])


""" The following functions are for debugging. """


from Operator import sub, dot, cross

def verify_volume(nodes, tetras):
    total = 0
    for t in tetras:
        A = nodes[t[0]]
        B = nodes[t[1]]
        C = nodes[t[2]]
        D = nodes[t[3]]
        total += abs(dot(sub(B,A), cross(sub(C,A), sub(D,A))))
    total /= 6.0
    print(total)

def load_single():
    nodes = np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]])
    tetras = np.array([[0,1,2,3]])
    SIZE = 1
    return nodes, tetras
