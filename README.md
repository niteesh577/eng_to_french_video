# 🎬 AI Video Dubber: English → French

A Streamlit-based web app that lets you upload an English video and get back a French-dubbed version with:
- Natural, AI-generated French audio (lip-synced to the original video)
- French subtitles only where English text is detected in the frames

---

## 🚀 Features
- **Automatic Speech Recognition (ASR):** Transcribes English speech using OpenAI Whisper
- **Translation:** Translates English to French using Gemini 2.0 Flash via LangChain
- **Text-to-Speech (TTS):** Generates high-quality French audio (ElevenLabs)
- **Lip Sync:** Aligns French audio to video using simplified Wav2Lip approach
- **OCR:** Detects English text in video frames (Tesseract)
- **Subtitles:** Translates detected text and overlays French subtitles only where needed
- **Streamlit UI:** Simple upload, progress bars, preview, and download

---

## 🗂️ Project Structure
```
ai_dubber_app/
│
├── streamlit_app.py             # Streamlit UI entry point
├── requirements.txt             # All dependencies
├── setup.py                    # Setup script
├── .env                         # For API keys
├── README.md                    # This file
│
├── config/
│   └── settings.py              # Loads .env, config vars
│
├── utils/
│   ├── transcription.py         # Whisper ASR
│   ├── ocr.py                   # Tesseract OCR
│   ├── translation.py           # LangChain + Gemini translation
│   ├── tts.py                   # TTS generation in French
│   ├── lip_sync.py              # Simplified lip-sync integration
│   ├── subtitles.py             # Subtitle creation and overlay
│   └── video_processing.py      # Frame extraction, audio/video recombination
│
├── Wav2Lip/
│   └── simple_inference.py      # Simplified lip-sync script
│
└── assets/
    └── sample_videos/           # For demo/testing
```

---

## ⚙️ Quick Setup
1. **Clone the repo**
2. **Run the setup script:**
   ```bash
   cd ai_dubber_app
   python setup.py
   ```
3. **Add your API keys** to `.env`:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```
4. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

---

## 🖥️ Usage
1. **Upload an English MP4 video**
2. **Wait for processing:**
   - Transcription
   - Translation
   - TTS
   - Lip Sync
   - OCR
   - Subtitle generation & overlay
3. **Preview and download** your French-dubbed video!

---

## 🛠️ Tech Stack
- [OpenAI Whisper](https://github.com/openai/whisper) (ASR)
- [LangChain](https://python.langchain.com/) + Gemini 2.0 Flash (Translation)
- [ElevenLabs](https://elevenlabs.io/) (TTS)
- Simplified Wav2Lip approach (Lip Sync)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (Text detection)
- [MoviePy](https://zulko.github.io/moviepy/) (Video processing)
- [pysrt](https://pypi.org/project/pysrt/) (Subtitles)
- [Streamlit](https://streamlit.io/) (UI)

---

## 📝 Credits & Inspiration
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) (simplified approach)
- [LangChain](https://python.langchain.com/)
- [ElevenLabs](https://elevenlabs.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [MoviePy](https://zulko.github.io/moviepy/)

---

## 📄 License
MIT License (see LICENSE)

---

## 🙋 FAQ
- **Q:** Can I use other languages?  
  **A:** The code is modular—add more translation/TTS logic for other languages!
- **Q:** Does it work offline?  
  **A:** Whisper and Tesseract can run locally, but translation and TTS require API access.
- **Q:** How do I get ElevenLabs or Gemini API keys?  
  **A:** Sign up at [ElevenLabs](https://elevenlabs.io/) and [Google AI Studio](https://aistudio.google.com/).
- **Q:** What if lip-sync fails?  
  **A:** The system falls back to simple audio replacement using ffmpeg.

---

## ✨ Contributing
PRs and suggestions welcome! Please open an issue or submit a pull request. 