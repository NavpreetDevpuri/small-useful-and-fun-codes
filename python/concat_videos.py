import glob
import sys
import os
import subprocess

path=""
if len(sys.argv) > 1:
    path=sys.argv[1]
videoList = glob.glob(os.path.join(path,"*.mp4"))
videoList.sort(key=os.path.getctime)
print("file '" + "'\nfile '".join(videoList) + "'")
with open("list.txt", "w") as listFile:
    listFile.write("file '" + "'\nfile '".join(videoList) + "'")
subprocess.call(['ffmpeg', '-f', 'concat',"-safe","0","-i","list.txt",'-c','copy', 'output.mp4'])
    