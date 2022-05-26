import numpy as np
import math
import constants
from timeit import default_timer as timer


class LocalizationMethods(object):
    def __init__(self):
        self.dmResult = None
        self.dmTime = 0
        self.lsmResult = None
        self.lsmTime = 0
        self.tsmResult = None
        self.tsmTime = 0

    def directMethod(self, distances: np.ndarray):
        start = timer()

        x2 = constants.X2
        x3 = constants.X3

        approxPos = np.empty(distances[1:3].shape)

        for i, (d1, d3) in enumerate(zip(distances[1], distances[2])):
            k2 = 0.5 * (d1**2 - x2**2)
            k3 = 0.5 * (d3**2 - x3**2)
            xApprox = (d1 * k3 - d3 * k2) / (d3 * x2 - d1 * x3)

            yApprox = math.sqrt(abs(((k2 + xApprox * x2) / d1)**2 - xApprox**2))

            approxPos[0][i] = xApprox
            approxPos[1][i] = yApprox

        end = timer()

        # Time in seconds
        self.dmTime = end - start

        self.dmResult = approxPos

    def lsMethod(self, distances: np.ndarray):
        start = timer()

        xApprox = np.zeros(distances[0].size)
        yApprox = np.zeros(distances[0].size)

        distTransp = distances.T

        for i in range(xApprox.size):
            xApprox[i] = self.calcLsmPosVector(distTransp[i])[0]
            yApprox[i] = self.calcLsmPosVector(distTransp[i])[1]

        end = timer()

        # Time in seconds
        self.lsmTime = end - start

        self.lsmResult = np.stack((xApprox, yApprox))

    def calcLsmPosVector(self, distances: list) -> np.ndarray:
        recieverVecX = [constants.X1, constants.X2, constants.X3, constants.X4]
        recieverVecY = [constants.Y1, constants.Y2, constants.Y3, constants.Y4]
        aMatrix = [[], []]
        bVector = []

        # Set first elipse as the reference elipse
        j = 0
        xj = recieverVecX[0]
        yj = recieverVecY[0]
        dj = distances[0]
        pj = 0.5 * (xj ** 2 + yj ** 2 - dj ** 2)

        # Calculate matrix A, vector b
        for i, (xi, yi, di) in enumerate(zip(recieverVecX, recieverVecY, distances)):
            if i == j:
                continue
            pi = 0.5 * (xi**2 + yi**2 - di**2)
            a1 = xi * dj - xj * di
            a2 = yi * dj - yj * di
            b = pi * dj - pj * di

            aMatrix[0].append(a1)
            aMatrix[1].append(a2)
            bVector.append(b)

        # Matrix A
        # Convert python list to np.ndarray
        a1Arr = np.array(aMatrix[0])
        a2Arr = np.array(aMatrix[1])
        aArr = np.vstack((a1Arr, a2Arr)).T

        # Vector b
        bArr = np.array(bVector).T

        # Calculate the resulting position vector p
        first = np.dot(aArr.T, aArr)
        firstInv = np.linalg.matrix_power(first, -1)
        second = np.dot(aArr.T, bArr)
        posVec = np.dot(firstInv, second)

        return posVec

    def tsMethod(self, distances: np.ndarray):
        start = timer()
        xApprox = np.zeros(distances[0].size)
        yApprox = np.zeros(distances[0].size)

        distTransp = distances.T

        for i in range(xApprox.size):
            xApprox[i] = self.calcTsmPosVector(distTransp[i])[0]
            yApprox[i] = self.calcTsmPosVector(distTransp[i])[1]

        end = timer()

        # Time in seconds
        self.tsmTime = end - start

        self.tsmResult = np.stack((xApprox, yApprox))

    def calcTsmPosVector(self, distances: list) -> tuple:
        xv = self.calcLsmPosVector(distances)[0]
        yv = self.calcLsmPosVector(distances)[1]

        for step in range(5):
            delta = self.calcDelta(distances, xv, yv)
            xv += delta[0]
            yv += delta[1]

        return xv, yv

    def calcDelta(self, distances: list, xv: float, yv: float) -> np.ndarray:
        recieverVecX = [constants.X1, constants.X2, constants.X3, constants.X4]
        recieverVecY = [constants.Y1, constants.Y2, constants.Y3, constants.Y4]
        aMatrix = [[], []]
        bVector = []

        for i, (xi, yi, di) in enumerate(zip(recieverVecX, recieverVecY, distances)):
            trans_dist = math.sqrt(xv ** 2 + yv ** 2)
            rec_dist = math.sqrt((xv - xi) ** 2 + (yv - yi) ** 2)

            a1 = (xv / trans_dist) + ((xv - xi) / rec_dist)
            a2 = (yv / trans_dist) + ((yv - yi) / rec_dist)
            fi = trans_dist + rec_dist
            b = di - fi

            aMatrix[0].append(a1)
            aMatrix[1].append(a2)
            bVector.append(b)

        # Matrix A
        # Convert python list to np.ndarray
        a1Arr = np.array(aMatrix[0])
        a2Arr = np.array(aMatrix[1])
        aArr = np.vstack((a1Arr, a2Arr)).T

        # Vector b
        bArr = np.array(bVector).T

        # Calculate the resulting delta vector
        first = np.dot(aArr.T, aArr)
        firstInv = np.linalg.matrix_power(first, -1)
        second = np.dot(aArr.T, bArr)
        delta = np.dot(firstInv, second)

        return delta

    def clearData(self):
        np.delete(self.dmResult, np.s_[::])
        np.delete(self.lsmResult, np.s_[::])
        np.delete(self.tsmResult, np.s_[::])
        self.dmTime = 0
        self.lsmTime = 0
        self.tsmTime = 0


def rawDist2Dist(positionData: list) -> np.ndarray:
    # Calculate r1, r2 for each t
    rawDistances = roomPos2RawDist(positionData)

    # Allocate new ndarray
    distances = np.empty(rawDistances.shape)

    # Calculate d1, d2 for each t
    if distances.size != 0:
        distances = addNoise2Data(rawDistances)

    return distances


def roomPos2RawDist(data: list) -> np.ndarray:
    pos = np.array(data)
    # noisedPos = addNoise2Pos(pos)
    rawDistances = np.empty((4, pos[0].size))

    for i, (x, y) in enumerate(zip(pos[0], pos[1])):
        rawDistances[0][i] = calcRi(x, y, constants.X1, constants.Y1)
        rawDistances[1][i] = calcRi(x, y, constants.X2, constants.Y2)
        rawDistances[2][i] = calcRi(x, y, constants.X3, constants.Y3)
        rawDistances[3][i] = calcRi(x, y, constants.X4, constants.Y4)

    return rawDistances


def addNoise2Pos(data: np.ndarray) -> np.ndarray:
    noisedData = np.empty(data.shape)
    noiseRaw = np.random.normal(0, 0.05, data[0].size)

    noisedData[0] = data[0] + noiseRaw
    noisedData[1] = data[1] + noiseRaw

    return noisedData

def calcRi(xt: float, yt: float, xi: float, yi: float) -> float:
    return math.sqrt(xt ** 2 + yt ** 2) + math.sqrt((xt - xi) ** 2 + (yt - yi) ** 2)


def addNoise2Data(data: np.ndarray) -> np.ndarray:
    noiseRaw = np.random.normal(0, 0.1, data[0].size)

    noisedDist1 = data[0] + noiseRaw
    noisedDist2 = data[1] + noiseRaw
    noisedDist3 = data[2] + noiseRaw
    noisedDist4 = data[3] + noiseRaw
    newArr = np.stack((noisedDist1, noisedDist2, noisedDist3, noisedDist4))

    return newArr
