from pdf2image import convert_from_path
from PIL import Image
import PIL.ImageOps 
import sys, os

os.makedirs("pyout", exist_ok=True)
os.makedirs(os.path.join("pyout","ztemp"), exist_ok=True)
size = (2480, 2480)
if sys.argv[1][-5] == "t": #rect
    size = (2480, 3508)
convert_from_path(sys.argv[1], output_folder="pyout", fmt="jpeg",size=size)
f = os.listdir("pyout")

for i in range(len(f)-1):
    filepath = os.path.join("pyout", sys.argv[1][:-4]+" %02d" % (i) +".jpeg")
    filesavepath = os.path.join("pyout", "ztemp", sys.argv[1][:-4]+" %02d" % (i) +".jpeg")
    os.replace(os.path.join("pyout", f[i]), filepath)
    PIL.ImageOps.invert(Image.open(filepath)).save(filesavepath)


    