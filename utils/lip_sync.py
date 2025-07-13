import logging
import subprocess
import os

logger = logging.getLogger(__name__)


def lip_sync_video(video_path: str, audio_path: str, output_path: str) -> str:
    """
    Lip-sync French audio to video using simplified Wav2Lip.
    Returns the path to the lip-synced video.
    """
    try:
        # Path to our simplified inference script
        wav2lip_script = os.path.join(os.path.dirname(__file__), "..", "Wav2Lip", "simple_inference.py")
        
        if not os.path.exists(wav2lip_script):
            logger.error(f"Wav2Lip script not found at {wav2lip_script}")
            # Fallback: just replace audio without lip-sync
            logger.info("Falling back to simple audio replacement...")
            return _simple_audio_replacement(video_path, audio_path, output_path)
        
        command = [
            "python3", wav2lip_script,
            "--face", video_path,
            "--audio", audio_path,
            "--outfile", output_path
        ]
        
        logger.info(f"Running lip-sync: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Lip-sync output: {result.stdout}")
        
        if os.path.exists(output_path):
            logger.info(f"Lip-synced video saved at {output_path}")
            return output_path
        else:
            logger.error("Lip-sync failed - output file not created")
            return _simple_audio_replacement(video_path, audio_path, output_path)
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Lip-sync subprocess failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return _simple_audio_replacement(video_path, audio_path, output_path)
    except Exception as e:
        logger.error(f"Lip sync failed: {e}")
        return _simple_audio_replacement(video_path, audio_path, output_path)


def _simple_audio_replacement(video_path: str, audio_path: str, output_path: str) -> str:
    """
    Simple fallback: replace audio in video using ffmpeg.
    """
    try:
        import subprocess
        command = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output_path
        ]
        
        logger.info(f"Running simple audio replacement: {' '.join(command)}")
        subprocess.run(command, check=True)
        logger.info(f"Audio-replaced video saved at {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Simple audio replacement failed: {e}")
        return "" 