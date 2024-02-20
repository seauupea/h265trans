import subprocess
import glob
import argparse
import os

def get_video_files(directory):
    """
    Retrieve video files of specified formats from the given directory.
    """
    extensions = ['*.mxf', '*.mp4', '*.mov', '*.mkv']
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, ext)))
    return files

def get_video_bitrate(video_path):
    """
    Use mediainfo to get the video bitrate of the video in Mbps.
    """
    command = ['mediainfo', '--Inform=Video;%BitRate%', video_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    bitrate_str = result.stdout.strip()

    try:
        # Convert bitrate from bits per second to Mbps
        bitrate_bps = int(bitrate_str)
        return bitrate_bps / 1000000  # Convert to Mbps
    except ValueError:
        # If conversion fails, print an error and return None
        print(f"Could not determine video bitrate for {video_path}. Mediainfo output: '{bitrate_str}'")
        return None

def calculate_optimal_bitrate(original_bitrate, reduction_factor=0.5625):
    """
    Calculate the optimal bitrate based on the original bitrate and a reduction factor.
    """
    return int(original_bitrate * reduction_factor)

def transcode_to_h265(source_path, output_path, optimal_bitrate, use_hw_accel):
    """
    Transcode a video file to H.265 using FFmpeg with the specified optimal bitrate.
    Optionally, use hardware acceleration if available on macOS.
    """
    command = [
        'ffmpeg',
        '-i', source_path,  # Input file
        '-c:v', 'hevc_videotoolbox' if use_hw_accel else 'libx265',  # Codec: H.265 with or without hardware acceleration
        '-b:v', f'{optimal_bitrate}M',  # Video bitrate in Mbps
        '-c:a', 'copy',  # Copy audio stream without re-encoding
    ]

    if use_hw_accel:
        command.extend(['-tag:v', 'hvc1'])  # Ensure compatibility with certain players

    command.append(output_path)  # Output file

    subprocess.run(command, check=True)

def main(args):
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    source_videos = get_video_files(args.input_dir)

    for video_path in source_videos:
        original_bitrate = get_video_bitrate(video_path)
        if original_bitrate is not None:
            optimal_bitrate = calculate_optimal_bitrate(original_bitrate, args.reduction_factor)
            output_filename = os.path.splitext(os.path.basename(video_path))[0] + '_transcoded.mp4'
            output_path = os.path.join(args.output_dir, output_filename)
            print(f'Transcoding {video_path} to {output_path} with optimal bitrate: {optimal_bitrate} Mbps')
            transcode_to_h265(video_path, output_path, optimal_bitrate, args.hw_accel)
        else:
            print(f"Could not determine video bitrate for {video_path}. Skipping.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Transcode videos to H.265 with an optimised bitrate. Optionally use hardware acceleration on macOS.")
    parser.add_argument("-i", "--input_dir", required=True, help="Directory containing source videos to transcode.")
    parser.add_argument("-o", "--output_dir", required=True, help="Directory where transcoded videos will be saved.")
    parser.add_argument("-r", "--reduction_factor", type=float, default=0.5625, help="Reduction factor for calculating the optimal bitrate.")
    parser.add_argument("-hw", "--hw_accel", action='store_true', help="Use hardware acceleration if available (macOS only).")

    args = parser.parse_args()

    main(args)
