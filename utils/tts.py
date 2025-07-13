import os, uuid, logging
from config import settings

logger = logging.getLogger(__name__)

def text_to_speech(text: str, output_folder: str) -> str:
    api_key = getattr(settings, "ELEVENLABS_API_KEY", None)
    if not api_key:
        logger.error("ELEVENLABS_API_KEY not set.")
        return ""

    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs import save
    except ImportError as e:
        logger.error(f"ElevenLabs SDK not found: {e}")
        return ""

    client = ElevenLabs(api_key=api_key)
    logger.info(f"Generating TTS for {len(text)} chars...")

    try:
        # List available voices
        voices_resp = client.voices.get_all()
        logger.debug(f"Found voices: {[v.name for v in voices_resp.voices]}")

        # Pick first voice supporting French
        from elevenlabs import Voice
        french_voice = next(
            (v for v in voices_resp.voices if any(
                lang.language.lower().startswith("fr")
                for lang in getattr(v, "verified_languages", [])
            )),
            None
        )
        if not french_voice:
            logger.error("No French-capable voice found.")
            return ""

        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id=french_voice.voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_22050_32",
        )

        os.makedirs(output_folder, exist_ok=True)
        filename = f"{uuid.uuid4()}.mp3"
        out_path = os.path.join(output_folder, filename)

        save(audio_stream, out_path)
        if os.path.isfile(out_path):
            logger.info(f"TTS saved: {out_path}")
            return out_path
        else:
            logger.error(f"Failed to create file at {out_path}")
            return ""
    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        return ""
