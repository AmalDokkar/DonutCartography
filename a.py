from PIL import Image, ImageDraw
import math, mpmath

# function for projection equations
def projectionCoordinates (theta, phi, signX, signY):
    x = R + (r * (2 / (math.tan(theta) + mpmath.sec(theta)))) *signY*math.sin(phi)
    y = R - (r * (2 / (math.tan(theta) + mpmath.sec(theta)))) *signX*math.cos(phi)
    return x, y

# function to get theta
def getTheta (x, phi, sign):
    # it's all rigth because we only want positive thetas
    k = ((x / sign * math.cos(phi)) - R) / r
    if (k < -1.0): k = -1.0 # because of floating point precision
    if (k > 1.0): k = 1     # this must be done
    theta = math.acos(k)
    return theta

# function that return quadrant given coordinates
def quadrant (x, y):
    if (x >= 0 and y >= 0): return 1
    elif (x < 0 and y >= 0): return 2
    elif (x < 0 and y < 0): return 3
    else: return 4

# this should be given by the user and computed by hand
R = int(input())
r = int(input())

X = int(input()) # coordinates of the center
Y = int(input())
# from pixels to cartesian coordinates sustract X, Y
# cartesian coordinates to pixels add X, Y respectively

# bounds of the map
MAXX = 2*(R + 2*r)
MAXY = 2*(R + 2*r)

# output image size [2(R+2r)+1, 2(R+2r)+1]
# dimensions [0..2(R+2r)][0..2(R+2r)]
inImg = Image.open(r"/home/amaldok/Prog/OIFem-LoC-2021-22/donut.jpg")

H, W = inImg.size # height and width of input image

outImg = Image.new('RGB', (MAXX + 1, MAXY + 1), 'Black')
dib = ImageDraw.Draw(outImg)

# interate through all pixels:
for i in range(0, H):
    for j in range(0, W):
        
        # cartesian coordinates
        inX = i - X
        inY = j - Y

        if r*r <= inX*inX + inY*inY <= R*R: # inside the donut
            # print(inX, inY) # to keep track of progress

            signX, signY, phi = 1, 1, 10000000000
            if (inX < 0): signX = -1    # sadly, in only gives positive values :(
            if (inY < 0): signY = -1
            if (inX != 0): phi = math.atan(inY / inX)   # not 100% sure about this

            theta = getTheta(inX, phi, signX)
            outX, outY = projectionCoordinates(theta, phi, signX, signY)
            print(outX, outY)
            
            if (quadrant(inX, inY) != quadrant(outX, outY)):
                continue

            outX += X   # important to add the center coordinates
            outY += Y   # to get the pixel's position!

            if 0 <= outX <= MAXX and 0 <= outY <= MAXY: # inside bounds
                color = inImg.getpixel((i, j))
                dib.point((outX, outY), color) # dib on outImg
    
outImg.save("out5.jpg")


"""
Test 1:
    R = 725
    r = 440
    X = 745
    Y = 725

c/p:
725
440
745
725
"""
