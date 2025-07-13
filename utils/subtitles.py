import logging
import pysrt
from moviepy.editor import VideoFileClip
import tempfile
import os

logger = logging.getLogger(__name__)

def generate_srt(subtitles, output_path):
    """
    Generate SRT file from subtitles.
    subtitles: list of (start, end, text) in seconds.
    output_path: path to save the .srt file.
    """
    try:
        subs = pysrt.SubRipFile()
        for idx, (start, end, text) in enumerate(subtitles, 1):
            sub = pysrt.SubRipItem(
                index=idx,
                start=pysrt.SubRipTime(seconds=int(start)),
                end=pysrt.SubRipTime(seconds=int(end)),
                text=text
            )
            subs.append(sub)
        subs.save(output_path, encoding='utf-8')
        logger.info(f"SRT file generated at {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"SRT generation failed: {e}")
        return ""

def burn_subtitles(video_path, srt_path, output_path):
    """
    Burn subtitles into video using MoviePy.
    Returns the path to the subtitled video.
    """
    try:
        # MoviePy does not natively burn SRT, so we use ffmpeg via subprocess
        import subprocess
        command = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"subtitles={srt_path}",
            "-c:a", "copy",
            output_path
        ]
        logger.info(f"Burning subtitles: {' '.join(command)}")
        subprocess.run(command, check=True)
        logger.info(f"Subtitled video saved at {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Subtitle burning failed: {e}")
        return "" 