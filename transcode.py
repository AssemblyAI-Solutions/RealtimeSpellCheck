import os
import subprocess

def convert_audio_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):  # Assuming we are converting .wav files
            # Constructing the full path for the input and output files
            input_file = os.path.join(folder_path, filename)
            output_file = os.path.join(folder_path, filename)

            # Running the FFmpeg command
            subprocess.run(["ffmpeg", "-i", input_file, "-acodec", "pcm_s16le", "-ar", "8000", output_file])

            # Removing the original file
            os.remove(input_file)

# Example usage
convert_audio_files("./audio")