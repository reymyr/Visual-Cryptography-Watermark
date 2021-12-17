import random
from PIL import Image

class VC:
  def __init__(self):
    self.white = [
      ((0, 1, 1, 0), (0, 1, 1, 0)),
      ((1, 0, 0, 1), (1, 0, 0, 1)),
      ((1, 0, 1, 0), (1, 0, 1, 0)),
      ((0, 1, 0, 1), (0, 1, 0, 1)),
      ((0, 0, 1, 1), (0, 0, 1, 1)),
      ((1, 1, 0, 0), (1, 1, 0, 0)),
    ]
    self.black = [
      ((0, 1, 1, 0), (1, 0, 0, 1)),
      ((1, 0, 0, 1), (0, 1, 1, 0)),
      ((1, 0, 1, 0), (0, 1, 0, 1)),
      ((0, 1, 0, 1), (1, 0, 1, 0)),
      ((0, 0, 1, 1), (1, 1, 0, 0)),
      ((1, 1, 0, 0), (0, 0, 1, 1)),
    ]

  def encrypt(self, img: Image.Image):
    img = img.convert('1')
    w, h = img.width * 2, img.height * 2

    out1 = Image.new('1', (w, h))
    out2 = Image.new('1', (w, h))
    
    for i in range(0, img.width):
      for j in range(0, img.height):
        # if black pixel
        if img.getpixel((i, j)) == 0:
          p1, p2 = random.choice(self.black)
        #if white
        else:
          p1, p2 = random.choice(self.white)

        out1.putpixel((i*2, j*2), p1[0])
        out1.putpixel((i*2+1, j*2), p1[1])
        out1.putpixel((i*2, j*2+1), p1[2])
        out1.putpixel((i*2+1, j*2+1), p1[3])

        out2.putpixel((i*2, j*2), p2[0])
        out2.putpixel((i*2+1, j*2), p2[1])
        out2.putpixel((i*2, j*2+1), p2[2])
        out2.putpixel((i*2+1, j*2+1), p2[3])

    return out1, out2

  def decrypt(self, img1: Image.Image, img2: Image.Image):
    img1 = img1.convert('1')
    img2 = img2.convert('1')

    out = Image.new('1', (img1.width, img1.height))

    for i in range(0, img1.width):
      for j in range(0, img1.height):
        out.putpixel((i, j), img1.getpixel((i, j)) * img2.getpixel((i, j)))
    
    return out

if __name__ == "__main__":
  vc = VC()

  img = Image.open("itb.jpg")

  out1, out2 = vc.encrypt(img)

  out1.save("1.png")
  out2.save("2.png")

  dec = vc.decrypt(out1, out2)
  
  dec.save("dec.png")