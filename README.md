# Video Transcoding to H.265

This project includes a Python script for transcoding video files to H.265 (HEVC) using FFmpeg, with optional hardware acceleration on macOS. It dynamically determines the video bitrate using MediaInfo and applies a reduction factor to calculate the optimal bitrate for the output video.

## Features

- Transcodes video files to H.265 codec.
- Dynamically calculates video bitrates using MediaInfo.
- Applies a reduction factor to determine the optimal output bitrate.
- Supports hardware acceleration on macOS (using VideoToolbox).
- Handles multiple video formats: MXF, MP4, MOV, MKV.

## Requirements

- Python 3.6 or higher
- FFmpeg
- MediaInfo

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.
2. Install FFmpeg and MediaInfo. These should be accessible from your system's PATH.
3. Clone this repository or download the script.


## Usage

Run the script with the following command, specifying the input and output directories, Optionally enabling hardware acceleration and/or manually setting the output filesize reduction factor:

```bash
python transcode2h265.py -i /path/to/source/videos -o /path/to/output/videos -hw -r 0.5625
```

Arguments:

- `-i`, `--input_dir`: Directory containing source videos to transcode.
- `-o`, `--output_dir`: Directory where transcoded videos will be saved.
- `-r`, `--reduction_factor`: (Optional) Reduction factor for calculating the optimal bitrate. Default is 0.5625.
- `-hw`, `--hw_accel`: (Optional) Use hardware acceleration if available (macOS only).

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is open source and available under the [MIT License](LICENSE).