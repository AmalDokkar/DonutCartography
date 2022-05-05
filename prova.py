from PIL import Image, ImageDraw

img = Image.new('RGB', (11, 11), 'Black')
dib = ImageDraw.Draw(img)

dib.ellipse((0, 0, 10, 10), 'White')
dib.ellipse((2, 2, 8, 8), 'Black')

img.save('test.png')


