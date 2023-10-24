import os
from moviepy.editor import VideoFileClip

# Function to compress a video file
def compress_video(input_file, output_file):
    video = VideoFileClip(input_file)
    compressed_video = video.write_videofile(output_file, codec='libx264', preset='medium', audio_codec='aac', audio_bitrate='192k')
    video.close()

# Function to process a directory
def process_directory(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if '_compressed' in filename:
                continue
            if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                input_file = os.path.join(root, filename)
                output_file = os.path.join(output_dir, os.path.relpath(input_file, input_dir))
                output_file = os.path.splitext(output_file)[0] + '_compressed.mp4'

                # Create the output directory if it doesn't exist
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                print(f"Compressing {input_file} to {output_file}")
                compress_video(input_file, output_file)
                os.remove(input_file)

if __name__ == "__main__":
    input_directory = "/Users/navpreetdevpuri/Documents/cros"  # Replace with your input directory
    output_directory = "/Users/navpreetdevpuri/Documents/cros"  # Replace with your output directory

    process_directory(input_directory, output_directory)
