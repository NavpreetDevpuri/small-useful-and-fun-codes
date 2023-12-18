import os
import subprocess
from concurrent.futures import ProcessPoolExecutor
from PIL import Image


# Function to compress a video file using FFmpeg
def compress_video(input_file, output_file):
    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-c:v",
        "libx264",
        "-crf",
        "28",
        "-preset",
        "veryslow",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        output_file,
    ]
    subprocess.run(cmd, check=True)


# Function to copy metadata
def copy_metadata(source_file, target_file):
    try:
        subprocess.run(
            [
                "exiftool",
                "-overwrite_original",
                "-TagsFromFile",
                source_file,
                "-all:all",
                target_file,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error copying metadata from {source_file} to {target_file}: {e}")


# Function to compress an image file
def compress_image(input_file, output_file):
    with Image.open(input_file) as img:
        img.save(output_file, quality=85, optimize=True)


# Function to process a single file
def process_file(root, filename, input_dir, output_dir):
    input_file = os.path.join(root, filename)
    output_file = os.path.join(output_dir, os.path.relpath(input_file, input_dir))

    if filename.endswith((".mp4", ".avi", ".mkv", ".mov")):
        output_file = os.path.splitext(output_file)[0] + "_compressed.mp4"
        compress_video(input_file, output_file)
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        output_file = os.path.splitext(output_file)[0] + "_compressed.jpg"
        compress_image(input_file, output_file)
    else:
        return

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print(f"Compressing {input_file} to {output_file}")
    copy_metadata(input_file, output_file)
    # os.remove(input_file)


# Function to process a directory using multiple processes
def process_directory(input_dir, output_dir):
    with ProcessPoolExecutor() as executor:
        for root, _, files in os.walk(input_dir):
            for filename in files:
                if "_compressed" in filename:
                    continue
                executor.submit(process_file, root, filename, input_dir, output_dir)


if __name__ == "__main__":
    input_directory = "/path/to/input"  # Replace with your input directory
    output_directory = "/path/to/output"  # Replace with your output directory

    process_directory(input_directory, output_directory)
