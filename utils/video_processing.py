import logging
import tempfile
import os
from moviepy.editor import VideoFileClip, AudioFileClip

logger = logging.getLogger(__name__)

def extract_audio(video_path):
    """
    Extract audio from video and return path to temporary audio file (wav).
    """
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
            audio_path = tmp_audio.name
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, logger=None)
        logger.info(f"Audio extracted to {audio_path}")
        return audio_path
    except Exception as e:
        logger.error(f"Audio extraction failed: {e}")
        return ""

def replace_audio(video_path, new_audio_path, output_path):
    """
    Replace original audio with new audio in video using ffmpeg.
    Returns the path to the new video file.
    """
    try:
        import subprocess
        command = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", new_audio_path,
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output_path
        ]
        logger.info(f"Replacing audio: {' '.join(command)}")
        subprocess.run(command, check=True)
        logger.info(f"Audio-replaced video saved at {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Audio replacement failed: {e}")
        return "" 