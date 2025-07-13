import logging
import cv2
import pytesseract
import numpy as np
from moviepy.editor import VideoFileClip
import tempfile
import os

logger = logging.getLogger(__name__)

# If Tesseract is not in your PATH, set it here (uncomment and edit as needed)
# pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Mac/Homebrew
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Windows

def preprocess_frame(frame):
    """
    Preprocess a frame for better OCR results.
    """
    image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)
    return gray

def detect_english_text_frames(video_path: str, frame_interval: float = 1.0, tesseract_timeout: int = 3):
    """
    Detect English text in video frames using Tesseract.
    Returns list of (frame_idx, text) for frames with detected English text.
    frame_interval: seconds between frames to check.
    tesseract_timeout: seconds to wait for Tesseract OCR per frame.
    """
    results = []
    try:
        video = VideoFileClip(video_path)
        duration = video.duration
        frame_count = int(duration // frame_interval)
        logger.info(f"Extracting {frame_count} frames for OCR...")

        for i in range(frame_count):
            t = i * frame_interval
            frame = video.get_frame(t)
            processed = preprocess_frame(frame)

            # Save frame to temp file for pytesseract
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
                frame_path = tmp_img.name
                cv2.imwrite(frame_path, processed)

            try:
                text = pytesseract.image_to_string(frame_path, lang="eng", timeout=tesseract_timeout).strip()
            except RuntimeError as timeout_error:
                logger.warning(f"Tesseract timeout on frame {i}: {timeout_error}")
                text = ""
            except Exception as e:
                logger.error(f"OCR failed on frame {i}: {e}")
                text = ""

            os.remove(frame_path)
            if text:
                logger.info(f"Frame {i}: Detected text: {text[:30]}...")
                results.append((i, text))

        logger.info(f"OCR complete. {len(results)} frames with English text detected.")
        return results
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return [] 