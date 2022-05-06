from cmath import sqrt
from PIL import Image, ImageDraw
import math, mpmath

# function for projection equations
def projectionCoordinates (theta, phi):
	# x = R * math.cos(phi) + (2*r / (math.tan(theta) + mpmath.sec(theta))) * math.sin(phi)
	# y = R * math.sin(phi) - (2*r / (math.tan(theta) + mpmath.sec(theta))) * math.cos(phi)
	a = (2 * r * math.cos(theta)) / (1 + math.sin(theta))
	x = (R + a) * math.cos(phi)
	y = (R + a) * math.sin(phi)
	return x, y

# function to get theta
def getTheta (x, y, phi):
	# it's all rigth because we only want positive thetas
	# k = (x / math.cos(phi) - R) / r
	# if (k < -1.0): k = -1.0 # because of floating point precision
	# if (k > 1.0): k = 1.0   # this must be done
	# theta = math.acos(k)
	# return theta

	l = (math.sqrt(x*x + y*y) - R) / r
	if l > 1.0: l = 1.0
	if l < -1.0: l = -1.0
	theta = math.acos(l)
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
inImg = Image.open(r"/home/helena/avla/donut.jpg")

H, W = inImg.size # height and width of input image

outImg = Image.new('RGB', (MAXX + 1, MAXY + 1), 'Black')
dib = ImageDraw.Draw(outImg)

# interate through all pixels:
for i in range(0, H):
	for j in range(0, W):
        
		# cartesian coordinates
		inX = i - X
		inY = j - Y
        
		# if quadrant(inX, inY) == 3 or quadrant(inX, inY) == 4:
		#     continue
		
		lo, hi = R-r, R+r
		
		if lo*lo <= inX*inX + inY*inY <= hi*hi: # inside the donut
			print(inX, inY) # to keep track of progress
			# dib.point((inX + MAXX//2, inY + MAXY//2), 'Pink')  

			phi = 10000000000
			# if (inX < 0): signX = -1    # sadly, in only gives positive values :(
			# if (inY < 0): signY = -1
			if (inX != 0.0): phi = math.atan(inY / inX)   # not 100% sure about this
            
			theta = getTheta(inX, inY, phi)
			# print(theta)
			outX, outY = projectionCoordinates(theta, phi)
			
			
			
			if quadrant(inX, inY) == 1 or quadrant(inX, inY) == 4:
				outX += MAXX//2   # important to add the center coordinates
				outY += MAXY//2   # to get the pixel's position!
				if 0 <= outX <= MAXX and 0 <= outY <= MAXY: # inside bounds
					color = inImg.getpixel((i, j))
					dib.point((outX, outY), color) # dib on outImg
			else:
				outX = MAXX//2 - outX
				outY = MAXY//2 - outY
				if 0 <= outX <= MAXX and 0 <= outY <= MAXY: # inside bounds
					color = inImg.getpixel((i, j))
					dib.point((outX, outY), color) # dib on outImg
				
for i in range(0, MAXX+1):
	for j in range(0, MAXY+1):
		color = outImg.getpixel((i, j))
		if color != (0, 0, 0): continue
		lo = 123
		hi = MAXX//2
		x = i-hi
		y = j-hi
		if hi*hi <= x*x + y*y or x*x + y*y <= lo*lo: continue
		
		n = 8
		finalR = 0
		finalG = 0
		finalB = 0
		
		c1 = (0, 0, 0)
		if i != 0 and j != 0:
			c1 = outImg.getpixel((i-1, j-1))
			finalR += c1[0]
			finalG += c1[1]
			finalB += c1[2]
		else: n -= 1
		
		c2 = (0, 0, 0)
		if i != 0:
			c2 = outImg.getpixel((i-1, j))
			finalR += c1[0]
			finalG += c1[1]
			finalB += c1[2]
		else: n -= 1
		
		c3 = (0, 0, 0)
		if i != 0 and j != MAXY:
			c3 = outImg.getpixel((i-1, j+1))
			finalR += c1[0]
			finalG += c1[1]
			finalB += c1[2]
		else: n -= 1
		
		c4 = (0, 0, 0)
		if j != 0:
			c4 = outImg.getpixel((i, j-1))
			finalR += c1[0]
			finalG += c1[1]
			finalB += c1[2]
		else: n -= 1
		
		c5 = (0, 0, 0)
		if j != MAXY:
			c5 = outImg.getpixel((i, j+1))
			finalR += c1[0]
			finalG += c1[1]
			finalB += c1[2]
		else: n -= 1
		
		c6 = (0, 0, 0)
		if i != MAXX and j != 0:
			c6 = outImg.getpixel((i+1, j-1))
			finalR += c1[0]
			finalG += c1[1]
			finalB += c1[2]
		else: n -= 1
		
		c7 = (0, 0, 0)
		if i != MAXX:
			c7 = outImg.getpixel((i+1, j))
			finalR += c1[0]
			finalG += c1[1]
			finalB += c1[2]
		else: n -= 1
		
		c8 = (0, 0, 0)
		if i != MAXX and j != MAXY:
			c8 = outImg.getpixel((i+1, j+1))
			finalR += c1[0]
			finalG += c1[1]
			finalB += c1[2]
		else: n -= 1
		
		if n != 0:
			finalR = finalR//n
			finalG = finalG//n
			finalB = finalB//n
		
		dib.point((i, j), (finalR, finalG, finalB))

outImg.save("fail11.jpg")


"""
Test 1:
    R = 725
    r = 220
    X = 745
    Y = 725
c/p:
505
222
726
746
"""
