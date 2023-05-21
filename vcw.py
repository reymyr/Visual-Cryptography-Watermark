import sys, argparse
from visual_cryptography import VC
from watermark import Watermarker
from PIL import Image

def main(argv):
  parser = argparse.ArgumentParser(description='Embed a watermark with visual cryptography.')

  parser.add_argument('-e', action='store_true', help='enable extraction mode')
  parser.add_argument('-i', action='store', help='input image to be watermarked/extracted', required=True)
  parser.add_argument('-o', action='store', help='output file name')
  parser.add_argument('-w', action='store', help='watermark image / share image if extract mode')
  
  args = parser.parse_args()

  vc = VC()
  watermarker = Watermarker()

  if args.e:
    img = Image.open(args.i)
    share2 = Image.open(args.w)
    share1 = watermarker.extractFragile(img)

    s2repeat = Image.new('1', (share1.width, share1.height))

    for i in range(0, share1.width, share2.width):
      for j in range(0, share1.height, share2.height):
        s2repeat.paste(share2, (i, j))

    extracted = vc.decrypt(share1, s2repeat)

    ofname = args.o if args.o else "extracted_watermark.png"      

    extracted.save(ofname)

  else:
    img = Image.open(args.i)
    wm = Image.open(args.w)

    share1, share2 = vc.encrypt(wm)

    wmimg = watermarker.embedFragile(img, share1)

    wmimg.save('watermarked_result.bmp')
    share1.save('share1.png')
    share2.save('share2.png')

if __name__ == '__main__':
  main(sys.argv[1:])

