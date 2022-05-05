from PIL import Image, ImageDraw

#per generar mini donuts x la forma

img = Image.new('RGB', (11, 11), 'Black')
dib = ImageDraw.Draw(img)

dib.ellipse((0, 0, 10, 10), 'White')
dib.ellipse((2, 2, 8, 8), 'Black')

img.save('test.png')


