import sys
import os
filePath=sys.argv[1]
os.system('ffmpeg -i ' + filePath + ' -vn -acodec pcm_s16le -ar 44100 -ac 2 '+os.path.basename(filePath)[0:-4]+'.wav')
