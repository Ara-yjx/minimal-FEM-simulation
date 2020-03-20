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


I3 = np.identity(3)

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
    return B, W # W might be negative




# constitutive law
def compute_P(F):
    # linear elasticity
    # return MU * (F + F.transpose() - 2 * I3) + LAMBDA * trace(F - I3) * I3
    # St. VK
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
        # FF.append([0,0,np.squeeze(F)[0][0]])
        H = - W[index] * P @ B[index].transpose()
        # h = np.squeeze(H)
        # f[t[0]] += H[0]
        # f[t[1]] += H[1]
        # f[t[2]] += H[2]
        # f[t[3]] += - H[0] - H[1] - H[2]

        h0 = np.array([H[0][0], H[1][0], H[2][0]])
        h1 = np.array([H[0][1], H[1][1], H[2][1]])
        h2 = np.array([H[0][2], H[1][2], H[2][2]])
        f[t[0]] += h0
        f[t[1]] += h1
        f[t[2]] += h2
        f[t[3]] += - h0 - h1 - h2
    return f



# stress derivative formula
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
        
        # df[t[0]] += dH[0]
        # df[t[1]] += dH[1]
        # df[t[2]] += dH[2]
        # df[t[3]] += - dH[0] - dH[1] - dH[2]

        dh0 = np.array([dH[0][0], dH[1][0], dH[2][0]])
        dh1 = np.array([dH[0][1], dH[1][1], dH[2][1]])
        dh2 = np.array([dH[0][2], dH[1][2], dH[2][2]])
        df[t[0]] += dh0
        df[t[1]] += dh1
        df[t[2]] += dh2
        df[t[3]] += - dh0 - dh1 - dh2

    return df


def negative_V(V):
    neg_V = []
    for v in V:
        neg_V.append(neg(v))
    # print(neg_V)
    return neg_V


def update_XV(def_X, T, V, B, W):
    Fe = compute_F(def_X, T, B, W)
    # Fd = - GAMMA * K(X*)V* = - GAMMA * df(dX=V)
    Fd = - GAMMA * np.array(compute_dF(def_X, negative_V(V), T, B, W))
    F = Fe + Fd
    # F = Fe
    
    # Naive Implicit Euler
    for i in range(len(def_X)):
        acceleration = F[i] / MASS
        acceleration += GRAVITY
        # v' = v + dt * F / M
        V[i] = add(V[i], DELTA_TIME * acceleration)
        # x' = x + dt * v
        def_X[i] = add(def_X[i], DELTA_TIME * V[i])

        # gound
        if def_X[i][2] < 0:
            def_X[i][2] = 0
            V[i][2] *= -COEF_OF_RESTITUTION
            # V[i][2] = 0

    return None
