from PIL import Image, ImageDraw
import math

R = int(input())
r = int(input())

def projectionCoordinates(theta, phi):
  x = (R + 2*r/(math.tan(theta)+math.sec(theta))) * math.sin(phi)
  y = (R - 2*r/(math.tan(theta)+math.sec(theta))) * math.cos(phi)
  return x, y

def getTheta(x, phi

siz = 2*(R + 2*r) + 1

image = Image.open('donut.jpg')

img = Image.new('RGB', (siz, siz), 'Black')
dib = ImageDraw.Draw(img)


