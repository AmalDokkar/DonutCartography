from PIL import Image, ImageDraw
from collections import deque
import math

def projectionCoordinates (theta, phi):
    a = (2 * r * math.cos(theta)) / (1 + math.sin(theta))
    x = (R + a) * math.cos(phi)
    y = (R + a) * math.sin(phi)
    return x, y

def getTheta (x, y, phi):
    l = (math.sqrt(x*x + y*y) - R) / r
    if l > 1.0: l = 1.0
    if l < -1.0: l = -1.0
    theta = math.acos(l)
    return theta

def quadrant (x, y):
    if (x >= 0 and y >= 0): return 1
    elif (x < 0 and y >= 0): return 2
    elif (x < 0 and y < 0): return 3
    else: return 4

R = int(input())
r = int(input())

X = int(input())
Y = int(input())

K = int(input())

MAX = 2*(R + 2*r)

inImg = Image.open(r"/home/amaldok/Prog/OIFem-LoC-2021-22/donut.jpg")

H, W = inImg.size

outImg = Image.new('RGB', (MAX + 1, MAX + 1), 'Black')
dib = ImageDraw.Draw(outImg)

for i in range(H):
    for j in range(W):
        
        inX = i - X
        inY = j - Y

        lo, hi = R-r, R+r
        if lo*lo <= inX*inX + inY*inY <= hi*hi:
            print(inX, inY)

            phi = 10000000000
            if (inX != 0.0): phi = math.atan(inY / inX)

            theta = getTheta(inX, inY, phi)
            outX, outY = projectionCoordinates(theta, phi)

            if quadrant(inX, inY) == 1 or quadrant(inX, inY) == 4:
                outX += MAX//2
                outY += MAX//2
                if 0 <= outX <= MAX and 0 <= outY <= MAX:
                    color = inImg.getpixel((i, j))
                    dib.point((outX, outY), color)
            else:
                outX = MAX//2 - outX
                outY = MAX//2 - outY
                if 0 <= outX <= MAX and 0 <= outY <= MAX:
                    color = inImg.getpixel((i, j))
                    dib.point((outX, outY), color)

bfs = deque()
u, v = [1, 0, -1, 0], [0, 1, 0, -1]

def black (x, y):
    r, g, b = outImg.getpixel((x, y))
    if r == 0 and g == 0 and b == 0:
        return True
    return False

def hasUncoloredNeighbours (x, y):
    for i in range(4):
        xi = x + u[i]
        yi = y + v[i]
        if (0 <= xi <= MAX and 0 <= yi <= MAX and black(xi, yi)):
            return True
    return False


for i in range(MAX+1):
    for j in range(MAX+1):
        if hasUncoloredNeighbours(i, j):
            color = outImg.getpixel((i, j))
            bfs.append((i, j, color))

while len(bfs) > 0:
    x, y, color = bfs.pop()
    if black(x, y):
        dib.point((x, y), color)

    for i in range(4):
        xi = x + u[i]
        yi = y + v[i]
        if (0 <= xi <= MAX and 0 <= yi <= MAX and black(xi, yi)):
            bfs.append((x, y, color))
    
outImg.save("out22.jpg")


"""

Test 1:
    R = 505
    r = 222
    X = 726
    Y = 726
    K = 123

c/p:

505
222
726
746
123

"""
