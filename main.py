from sympy import *
from sympy.geometry import *
import time
import random
import math
import matplotlib.pyplot as plt

test_1 = [
    Point(0, 0),
    Point(1, 0),
    Point(3, 0),
    Point(4, 0),
    Point(0, 4),
    Point(4, 1),
    Point(1, 4),
    Point(4, 4),
    Point(1, 2),
    Point(4, 2),
    Point(-1, 3),
    Point(-2, 2),
    Point(-1, 0),
    Point(2, 0)
]  # Colinear case

test_2 = []  # Randomly generated 10 test points
for i in range(10):
    test_2.append(Point(random.randint(-50, 50), random.randint(-50, 50)))

test_4 = []  # Randomly generated 100 test points
for i in range(100):
    test_4.append(Point(random.randint(-50, 50), random.randint(-50, 50)))


test_3 = [
    Point(0, 0),
    Point(1, 0),
    Point(0, 4),
    Point(4, 1),
    Point(4, 4),
    Point(1, 2),
    Point(-1, 5),
    Point(-2, 2)
]  # Points in general position

#### Animations ####
fig = plt.figure()
ax = fig.add_subplot(111)
xsc, ysc = zip(*test_1)


def init():
    ax.scatter(xsc, ysc, c="pink")


def animate(xs, ys):
    i = len(xs) - 1
    ax.cla()  # clear the previous image
    init()
    ax.plot(xs[:i], ys[:i], c="red")  # plot the line
    ax.plot(xs[i - 1:], ys[i - 1:], c="blue")
    fig.canvas.draw()
    fig.canvas.flush_events()


def getArcCosine(start, test):
    """
  This function returns the arccosine value between the bottommost point and the test point
  start, test: 2DPoint object
  """
    if start == test:
        return -math.inf
    else:
        return math.acos(
            (start[0] - test[0]) / (sqrt((start[0] - test[0])**2 +
                                         (start[1] - test[1])**2)))


def sortByAngle(pointList):
    """
  This function sorts the list of points by angles.
  """
    start = getBottomMost(pointList)
    angleDict = {}
    for i in pointList:
        angle = getArcCosine(start, i)
        angleDict[i] = angle

    sortedAngleDict = dict(
        sorted(angleDict.items(),
               key=lambda x: (x[1], (x[0][0]**2 + x[0][1]**2)))
    )  # sort by angle first, when tie, sort by distance

    sortedPointList = list(sortedAngleDict.keys())

    return sortedPointList


def getBottomMost(pointList):
    """
  This function finds the bottom left-most point
  """
    return (sorted(pointList, key=lambda x: (x[1], x[0]))[0])


def isLeftTurn(P1, P2, P3):
    """
  P1, P2, P3: individual point objects arranged ccw
  This function returns twice the signed area of the triangle determined by P1, P2, P3. The area is positive if P3 is on the left of P1, P2, negative if P3 is on the right of P1, P2, and zero if the points are collinear.
  """
    return (P2[0] - P1[0]) * (P3[1] - P1[1]) - (P3[0] - P1[0]) * (
        P2[1] - P1[1]) >= 0  #Colinear points on the hull


def grahamScan(pointList):
    # start a loop from the bottommost point, visiting points in the order of PointsToVisit
    sortedPointList = sortByAngle(pointList)
    pointsOnHull = []

    for x in sortedPointList:
        pointsOnHull.append(x)
        time.sleep(0.5)
        xs, ys = zip(*pointsOnHull)
        animate(xs, ys)

        while len(pointsOnHull) > 2 and isLeftTurn(
                pointsOnHull[-3], pointsOnHull[-2], pointsOnHull[-1]):
            pointsOnHull.pop(-2)
            time.sleep(0.5)
            xs, ys = zip(*pointsOnHull)
            animate(xs, ys)

        time.sleep(0.5)
        xs, ys = zip(*pointsOnHull)
        animate(xs, ys)

    pointsOnHull.append(sortedPointList[0])
    time.sleep(0.5)
    xs, ys = zip(*pointsOnHull)
    animate(xs, ys)
    return pointsOnHull


init()
plt.show(block=False)

hull = grahamScan(test_1)
xs, ys = zip(*hull)

print("Points on Hull:", hull)
