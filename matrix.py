import math
import constants as CONSTANTS

from pygame import Vector3


class Mat4:
    __slots__ = ['rows', 'cols', 'mat']

    def __init__(self, mat):
        self.mat = mat 

        a, b, c, d = mat
        self.cols = [
                 (Vector3((a[0], b[0], c[0])), d[0]),
                 (Vector3((a[1], b[1], c[1])), d[1]),
                 (Vector3((a[2], b[2], c[2])), d[2]),
                 (Vector3((a[3], b[3], c[3])), d[3])
             ]

    def vec_dot(self, vec):
        a, b, c, d = self.cols
        _vd = vec.dot
        return      Vector3(
                    _vd(a[0]) + a[1],
                    _vd(b[0]) + b[1],
                    _vd(c[0]) + c[1],
                        ), _vd(d[0]) + d[1]


    def mat4_dot(self, other):
        new_mat = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_mat[i][j] = sum([self.mat[i][k] * other.mat[k][j] for k in range(4)])
                # for k in range(4):
                    # new_mat[i][j] += self.mat[i][k] * other.mat[k][j]
        return Mat4(new_mat)



def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    m = m.mat
    determinant = getMatrixDeternminant(m)
    # if len(m) == 2:
        # return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                # [-1*m[1][0]/determinant, m[0][0]/determinant]]

    cofactors = []
    for r in range(4):
        cofactorRow = []
        for c in range(4):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = list(transposeMatrix(cofactors))
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return Mat4(cofactors)


def get_yaw(angle):
    cos = math.cos(angle)
    sin = math.sin(angle)
    return Mat4([
        [cos, sin, 0, 0],
        [-sin, cos, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])


def get_roll(angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        return Mat4([
            [1, 0, 0, 0],
            [0, cos, sin, 0],
            [0, -sin, cos, 0],
            [0, 0, 0, 1],
        ])

def get_pitch(angle):
    cos = math.cos(angle)
    sin = math.sin(angle)
    return Mat4([
        [cos, 0, -sin, 0],
        [0, 1, 0, 0],
        [sin, 0, cos, 0],
        [0, 0, 0, 1],
    ])


def get_translation_mat(x, y, z):
        return Mat4([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1]
            ])
