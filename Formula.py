""" All the physical formulae. You are not expected to understand these. """
""" ...unless you read the paper. """

import numpy as np
from numpy.linalg import inv, det
from Operator import add, neg, trace


MU = 0.3
LAMBDA = 0.3
GAMMA = 8
DELTA_TIME = 1
MASS = 20 # smaller mass, faster

GRAVITY = np.array([0, 0, -0.0002])
COEF_OF_RESTITUTION = 0

I3 = np.identity(3) # for acceleration


def precompute(X, T):
    B = []
    W = []
    for t in T:
        i = X[t[0]]
        j = X[t[1]]
        k = X[t[2]]
        l = X[t[3]]
        D = np.array([[ i[0]-l[0], j[0]-l[0], k[0]-l[0] ],
                      [ i[1]-l[1], j[1]-l[1], k[1]-l[1] ],
                      [ i[2]-l[2], j[2]-l[2], k[2]-l[2] ]])
        B.append(inv(D))
        W.append(abs(det(D) / 6.0))
    return B, W



def compute_P(F):
    E = 0.5 * (F.transpose() @ F - I3)
    P = F @ (2 * MU * E + LAMBDA * trace(E) * I3)
    return P



def compute_F(def_X, T, B, W):
    f = np.zeros((len(def_X), 3))
    for index, t in enumerate(T):
        i = def_X[t[0]]
        j = def_X[t[1]]
        k = def_X[t[2]]
        l = def_X[t[3]]
        D = np.array([[ i[0]-l[0], j[0]-l[0], k[0]-l[0] ],
                      [ i[1]-l[1], j[1]-l[1], k[1]-l[1] ],
                      [ i[2]-l[2], j[2]-l[2], k[2]-l[2] ]])
        
        F = D @ B[index]
        P = compute_P(F)
        H = - W[index] * P @ B[index].transpose()

        H = H.transpose()
        f[t[0]] += H[0]
        f[t[1]] += H[1]
        f[t[2]] += H[2]
        f[t[3]] += - H[0] - H[1] - H[2]
    return f



def compute_dP(F, dF):
    # St. VK
    E = 0.5 * (F.transpose() @ F - I3)
    dE = 0.5 * (dF.transpose() @ F + F.transpose() @ dF)
    dP = dF @ (2*MU*E + LAMBDA*trace(E)*I3) + F @ (2*MU*dE + LAMBDA*trace(dE)*I3)
    return dP



def compute_dF(def_X, dX, T, B, W):
    df = np.zeros((len(def_X), 3))
    for index, t in enumerate(T):
        i = def_X[t[0]]
        j = def_X[t[1]]
        k = def_X[t[2]]
        l = def_X[t[3]]
        D = np.array([[ i[0]-l[0], j[0]-l[0], k[0]-l[0] ],
                      [ i[1]-l[1], j[1]-l[1], k[1]-l[1] ],
                      [ i[2]-l[2], j[2]-l[2], k[2]-l[2] ]])
        i = dX[t[0]]
        j = dX[t[1]]
        k = dX[t[2]]
        l = dX[t[3]]
        dD = np.array([[ i[0]-l[0], j[0]-l[0], k[0]-l[0] ],
                       [ i[1]-l[1], j[1]-l[1], k[1]-l[1] ],
                       [ i[2]-l[2], j[2]-l[2], k[2]-l[2] ]])
        
        F = D @ B[index]
        dF = dD @ B[index]
        dP = compute_dP(F, dF)
        dH = - W[index] * dP @ (B[index].transpose())
        
        dH = dH.transpose()
        df[t[0]] += dH[0]
        df[t[1]] += dH[1]
        df[t[2]] += dH[2]
        df[t[3]] += - dH[0] - dH[1] - dH[2]

    return df



def negative_V(V):
    return [ neg(v) for v in V ]



def update_XV(def_X, T, V, B, W):
    Fe = compute_F(def_X, T, B, W)
    # Fd = - GAMMA * K(X*)V* = - GAMMA * df(dX=V)
    Fd = - GAMMA * compute_dF(def_X, negative_V(V), T, B, W)
    F = Fe + Fd
    
    # Naive Implicit Euler
    for i in range(len(def_X)):
        acceleration = F[i] / MASS + GRAVITY
        # v' = v + dt * F / M
        V[i] = add(V[i], DELTA_TIME * acceleration)
        # x' = x + dt * v
        def_X[i] = add(def_X[i], DELTA_TIME * V[i])

        # Gound collision
        if def_X[i][2] < 0: # if a node collides with the ground
            def_X[i][2] = 0  # it will be forced to move above the ground
            V[i][2] *= -COEF_OF_RESTITUTION # and it's z-velocity is inversed by "coefficient of restitution"

    return F
