from PIL import Image, ImageDraw
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

R = int(input("Enter the bigger radius of the torus (R): "))
r = int(input("The smaller radius (r): "))
X = int(input("Enter the X coordinate of the center: "))
Y = int(input("The Y coordinate of the center: "))
path = input("Enter the path of the input image (including the extension): ")
MAX = 2*(R + 2*r)

inImg = Image.open(path)
H, W = inImg.size
outImg = Image.new('RGB', (MAX + 1, MAX + 1), 'Black')
dib = ImageDraw.Draw(outImg)
u, v = [1, 1, 1, 0, 0, -1, -1, -1], [-1, 0, 1, -1, 1, -1, 0, 1]

print("Generating projection...")
for i in range(H):
    for j in range(W):
        inX = i - X
        inY = j - Y
        lo, hi = R-r, R+r

        if lo*lo <= inX*inX + inY*inY <= hi*hi:
            phi = 10000000000
            if (inX != 0.0): phi = math.atan(inY / inX)
            theta = getTheta(inX, inY, phi)
            outX, outY = projectionCoordinates(theta, phi)

            if quadrant(inX, inY) == 1 or quadrant(inX, inY) == 4:
                outX += MAX/2
                outY += MAX/2
                if 0 <= outX <= MAX and 0 <= outY <= MAX:
                    color = inImg.getpixel((i, j))
                    dib.point((outX, outY), color)
            else:
                outX = MAX/2 - outX
                outY = MAX/2 - outY
                if 0 <= outX <= MAX and 0 <= outY <= MAX:
                    color = inImg.getpixel((i, j))
                    dib.point((outX, outY), color)

outImg.save("projection.jpg")
print("Done")
print("Filling...")

def inBounds (x, y):
    if (x < 0 or y < 0 or x > MAX or y > MAX): return False
    return True

def black (x, y):
    r, g, b = outImg.getpixel((x, y))
    if r == 0 and g == 0 and b == 0:
        return True
    return False

for i in range(MAX+1):
    for j in range(MAX+1):
        if (i-MAX/2)**2 + (j-MAX/2)**2 > (MAX/2)**2: continue
        if not black(i, j): continue
        r, g, b, n = 0, 0, 0, 0

        for k in range(8):
            x = i + u[k]
            y = j + v[k]
            if not inBounds(x, y): continue
            color = outImg.getpixel((x, y))
            if color != (0, 0, 0):
                r, g, b, n = r+color[0], g+color[1], b+color[2], n+1
        if n != 0:
            r, g, b = r//n, g//n, b//n
            dib.point((i, j), (r, g, b))
    
outImg.save("filled.jpg")
print("Done. Check the current directory")

# /home/amaldok/Downloads/
