from PIL import Image

def modifyLSB(n, x):
  return (n & ~1) | (x & 1)

def extractLSB(n):
  return (n & 1) * 255

class Watermarker:
  def embedFragile(self, img: Image.Image, watermark: Image.Image):
    img = img.convert("RGB")
    w, h = img.size

    wmrepeat = Image.new('1', (w, h))

    for i in range(0, w, watermark.width):
      for j in range(0, h, watermark.height):
        wmrepeat.paste(watermark, (i, j))

    wmrepeat = wmrepeat.convert("RGB")
    
    for i in range(0, w):
      for j in range(0, h):
        oldpixel = img.getpixel((i, j))
        wmpixel = wmrepeat.getpixel((i, j))
        newpixel = tuple(map(modifyLSB, oldpixel, wmpixel))

        img.putpixel((i, j), newpixel)

    return img

  def extractFragile(self, img: Image.Image):
    w, h = img.size

    extracted = Image.new('RGB', (w, h))

    for i in range(0, w):
      for j in range(0, h):
        newpixel = tuple(map(extractLSB, img.getpixel((i, j))))
        extracted.putpixel((i, j), newpixel)
    
    extracted = extracted.convert('1')
    return extracted

if __name__ == '__main__':
  watermarker = Watermarker()
  img = Image.open('png_image_sample.png')
  wm = Image.open('2.png')
  wmimg = watermarker.embedFragile(img, wm)
  ext = watermarker.extractFragile(wmimg)
  ext.save("extracted.png")
