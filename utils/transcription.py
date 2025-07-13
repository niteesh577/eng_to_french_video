import logging
import os
import tempfile
from moviepy.editor import VideoFileClip

logger = logging.getLogger(__name__)

def transcribe_audio(video_path: str):
    """
    Transcribe English speech from video using Whisper.
    Returns transcript (str) and segments (list of dicts with 'start', 'end', 'text').
    """
    try:
        # Try to import whisper
        try:
            import whisper
        except ImportError as e:
            logger.error(f"Whisper import failed: {e}")
            return _fallback_transcription(video_path)
        
        # Extract audio to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
            audio_path = tmp_audio.name
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, logger=None)

        # Load Whisper model (use 'base' for speed, 'small' or 'medium' for accuracy)
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="en")
        transcript = result["text"]
        segments = result.get("segments", [])

        # Clean up temp audio
        os.remove(audio_path)
        logger.info("Transcription complete. Length: %d chars", len(transcript))
        return transcript, segments
        
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        return _fallback_transcription(video_path)

def _fallback_transcription(video_path: str):
    """
    Fallback transcription method when Whisper is not available.
    Returns a placeholder transcript for testing.
    """
    logger.warning("Using fallback transcription - please install Whisper for full functionality")
    return "Hello, this is a test transcript. Please install Whisper for proper transcription.", []

def extract_audio_only(video_path: str):
    """
    Extract audio from video without transcription.
    Returns the path to the extracted audio file.
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