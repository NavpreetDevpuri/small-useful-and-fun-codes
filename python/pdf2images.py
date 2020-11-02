from pdf2image import convert_from_path
import sys, os
os.makedirs("pyout", exist_ok=True)
convert_from_path(sys.argv[1], output_folder="pyout", fmt="jpeg")
