# Pitch Visualizer

This is a small Python script that visualizes the pitch of a pure vocal audio, merges it with the original video, and ultimately generates a video with dynamic pitch annotations.

## Usage

You need to prepare two files:

* Original video file (.mp4)
* Isolated vocal audio file extracted from the original video (.mp3)

To accurately draw pitch comparisons, you need to know the key of the song (e.g., C or F#). In this software, we do not specifically distinguish between major and minor keys; the key is only for annotating the scale. If the song is in a minor key, use the key of the corresponding major scale. For example, A minor corresponds to C.

```bash
python gen_pitch.py --audio <voice.mp3> -t <tone> <video.mp3> -o <output.mp4>

# Example
python gen_pitch.py --audio wjk_raw.mp3 -t E wjk.mp4 -o wjk_with_pitch.mp4
```

The `-o` option can be omitted, and it defaults to creating another video in the input video's folder.

### Other Options

* `--ffmpeg` allows you to specify the ffmpeg executable, necessary when ffmpeg is not in your PATH.
* `--pitch_width` sets the width of the pitch graph, defaulting to half the width of the original video.
* `--pitch_position` sets the position of the pitch graph, defaulting to `top_right`.
* `--min_pitch` sets the minimum recognized pitch, defaulting to `D2`.
* `--max_pitch` sets the maximum recognized pitch, defaulting to `G5`.

If you are familiar with the song's vocal range, adjusting `--min_pitch` and `--max_pitch` can enhance pitch recognition accuracy and speed up rendering.