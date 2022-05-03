from PIL import Image, ImgDraw
import math

R = int(input())
r = int(input())

# function for projection equations
def projectionCoordinates (theta: float, phi: float):
    x = (R + r * (2 / (math.tan(theta) + math.sec(theta)))) * math.sin(phi)
    y = (R - r * (2 / (math.tan(theta) + math.sec(theta)))) * math.cos(phi)
    return (x, y)

# function to get theta

# output image size [2(R+2r)+1, 2(R+2r)+1]
# dimensions [0..2(R+2r)][0..2(R+2r)]
X, Y = R + 2*r
# from pixels to cartesian coordinates sustract X, Y
# cartesian coordinates to pixels add X, Y respectively

inImg = Image.open(r"fileDirectory.extension")
outImg = Image.new('RGB', (2*X + 1, 2*Y + 1), 'Black')
dib = ImageDraw.Draw(outImg)


