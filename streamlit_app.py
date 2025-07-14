import streamlit as st
import os
import uuid
from utils import transcription, translation, tts, lip_sync, ocr, subtitles
from ai_dubber_app.config import settings

st.set_page_config(page_title="AI Video Dubber", layout="centered")
st.title("🎬 AI Video Dubber: English → French")

uploaded_file = st.file_uploader("Upload an English video (MP4)", type=["mp4"])

if uploaded_file:
    # 1. Save uploaded file
    session_id = str(uuid.uuid4())
    session_dir = f"output/{session_id}"
    os.makedirs(session_dir, exist_ok=True)

    input_video_path = os.path.join(session_dir, uploaded_file.name)
    with open(input_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.video(input_video_path)
    st.success(f"Video saved to {input_video_path}")

    # 2. Transcription
    with st.spinner("Transcribing audio..."):
        transcript, segments = transcription.transcribe_audio(input_video_path)
    if not transcript:
        st.error("❌ Transcription failed!")
        st.stop()
    st.success("✅ Transcription complete!")

    # 3. Translation
    with st.spinner("Translating to French..."):
        french_text = translation.translate_text(transcript)
    if not french_text:
        st.error("❌ Translation failed!")
        st.stop()
    st.success("✅ Translation complete!")

    # 4. TTS
    tts_audio_path = os.path.join(session_dir, "tts_audio.wav")
    with st.spinner("Generating French TTS..."):
        tts_audio_path = tts.text_to_speech(french_text, tts_audio_path)
    if not os.path.exists(tts_audio_path):
        st.error("❌ TTS generation failed!")
        st.stop()
    st.success("✅ TTS audio generated!")

    # 5. Lip Sync
    synced_video_path = os.path.join(session_dir, "synced_video.mp4")
    with st.spinner("Lip-syncing video..."):
        synced_video_path = lip_sync.lip_sync_video(input_video_path, tts_audio_path, synced_video_path)
    if not os.path.exists(synced_video_path):
        st.error("❌ Lip-sync failed!")
        st.stop()
    st.success("✅ Lip-sync complete!")

    # 6. OCR
    with st.spinner("Detecting English text in video frames..."):
        ocr_results = ocr.detect_english_text_frames(input_video_path)
    st.success(f"✅ OCR complete! Detected {len(ocr_results)} text frames.")

    # 7. Generate subtitles
    if ocr_results:
        subtitle_items = [(frame_idx, frame_idx+1, text) for frame_idx, text in ocr_results]
        srt_path = os.path.join(session_dir, "subtitles.srt")
        with st.spinner("Generating subtitles..."):
            srt_path = subtitles.generate_srt(subtitle_items, srt_path)
        if not os.path.exists(srt_path):
            st.error("❌ Subtitle generation failed!")
            st.stop()
        st.success("✅ Subtitles generated!")

        # 8. Burn subtitles
        final_video_path = os.path.join(session_dir, "final_video.mp4")
        with st.spinner("Burning subtitles into video..."):
            final_video_path = subtitles.burn_subtitles(synced_video_path, srt_path, final_video_path)
        if not os.path.exists(final_video_path):
            st.error("❌ Burning subtitles failed!")
            st.stop()
        st.success("✅ Final video ready with subtitles!")
    else:
        final_video_path = synced_video_path
        st.warning("⚠️ No English text detected for subtitles. Returning dubbed video without subtitles.")

    # 9. Display final video
    st.video(final_video_path)
    st.download_button(
        "Download French-dubbed video",
        data=open(final_video_path, "rb").read(),
        file_name="dubbed_french.mp4"
    )
