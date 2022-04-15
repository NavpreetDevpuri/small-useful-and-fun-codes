import glob
import sys
import os
import subprocess


def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


filePath = sys.argv[1]
timeStr = sys.argv[2]

temp = timeStr.split(":")

timeSec = (int(temp[0]) * 60 * 60 + int(temp[1])) * 60 + int(temp[2])
vLenSec = get_length(filePath)

output_file_path = 'fast_' + \
    os.path.basename(filePath)[0:-4]+"_x"+str(round(vLenSec/timeSec))+'.mp4'

subprocess.call(['ffmpeg', '-i', filePath, "-filter:v",
                "setpts=PTS/"+str(vLenSec/timeSec), output_file_path])
subprocess.call(['ffmpeg', '-y', '-ss', '00:00:00', '-to', timeStr, '-i', output_file_path, '-c', 'copy', output_file_path[0:-4]+'_cropped.mp4'])
