""" All the physical formulae. Including Alg 1 and 2 in paper. """

import numpy as np
from numpy.linalg import inv, det

from Operator import add


MU = 1
LAMBDA = 1
GAMMA = 1
DELTA_TIME = 1
MASS = 100

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
    # return MU * (F + F.transpose() - 2 * np.identity(3)) + LAMBDA * np.trace(F - np.identity(3)) * np.identity(3)
    # St. VK
    E = 0.5 * (F.transpose() @ F - np.identity(3))
    P = F @ (2 * MU * E + LAMBDA * np.trace(E) * np.identity(3))
    return P



def compute_F(def_X, T, B, W):
    f = np.zeros((len(def_X), 3))
    for index in range(len(T)):
        i = def_X[T[index][0]]
        j = def_X[T[index][1]]
        k = def_X[T[index][2]]
        l = def_X[T[index][3]]
        D = np.array([[ i[0]-l[0], j[0]-l[0], k[0]-l[0] ],
                      [ i[1]-l[1], j[1]-l[1], k[1]-l[1] ],
                      [ i[2]-l[2], j[2]-l[2], k[2]-l[2] ]])
        
        F = D @ B[index]
        P = compute_P(F)
        # FF.append([0,0,np.squeeze(F)[0][0]])
        H = - W[index] * P @ B[index].transpose()
        # h = np.squeeze(H)
        f[T[index][0]] += H[0]
        f[T[index][1]] += H[1]
        f[T[index][2]] += H[2]
        f[T[index][3]] += - H[0] - H[1] - H[2]
    return f



# stress derivative formula
def compute_dP(F, dF):
    # St. VK
    E = 0.5 * (F.transpose() @ F - np.identity(3))
    dE = 0.5 * (dF.transpose() @ F + F.transpose() @ dF)
    dP = dF @ (2*MU*E + LAMBDA*np.trace(E)*np.identity(3)) + F @ (2*MU*dE + LAMBDA*np.trace(dE)*np.identity(3))
    return dP



def compute_dF(def_X, dX, T, B, W):
    df = np.zeros((len(def_X), 3))
    for index in range(len(T)):
        i = def_X[T[index][0]]
        j = def_X[T[index][1]]
        k = def_X[T[index][2]]
        l = def_X[T[index][3]]
        D = np.array([[ i[0]-l[0], j[0]-l[0], k[0]-l[0] ],
                      [ i[1]-l[1], j[1]-l[1], k[1]-l[1] ],
                      [ i[2]-l[2], j[2]-l[2], k[2]-l[2] ]])
        i = dX[T[index][0]]
        j = dX[T[index][1]]
        k = dX[T[index][2]]
        l = dX[T[index][3]]
        dD = np.array([[ i[0]-l[0], j[0]-l[0], k[0]-l[0] ],
                       [ i[1]-l[1], j[1]-l[1], k[1]-l[1] ],
                       [ i[2]-l[2], j[2]-l[2], k[2]-l[2] ]])
        
        F = D @ B[index]
        dF = dD @ B[index]
        dP = compute_dP(F, dF)
        dH = - W[index] * dP @ B[index].transpose()
        
        df[T[index][0]] += dH[0]
        df[T[index][1]] += dH[1]
        df[T[index][2]] += dH[2]
        df[T[index][3]] += - dH[0] - dH[1] - dH[2]

    return df



def update_XV(def_X, T, V, B, W):
    Fe = compute_F(def_X, T, B, W)
    # Fd = - GAMMA * K(X*)V* = - GAMMA * df(dX=V)
    Fd = - GAMMA * np.array(compute_dF(def_X, V, T, B, W))
    F = Fe + Fd
    
    # Naive Implicit Euler
    for i in range(len(def_X)):
        # v' = v + dt * F / M
        V[i] = add(V[i], DELTA_TIME * F[i] / MASS)
        # x' = x + dt * v
        def_X[i] = add(def_X[i], DELTA_TIME * V[i])


    return Fe
