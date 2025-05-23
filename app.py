import streamlit as st
import os
import time
from datetime import datetime
from gtts import gTTS
from googletrans import Translator
from langdetect import detect, LangDetectException
import speech_recognition as sr
import pygame

# --- Functions ---
def recognize_speech(lang_code="en-US"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎙️ Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=lang_code)
        st.success(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("❌ Could not understand audio.")
    except sr.RequestError as e:
        st.error(f"❌ Speech Recognition failed: {e}")
    return None

def translate_text(text, target_lang):
    try:
        translator = Translator()
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        st.error(f"❌ Translation failed: {e}")
        return None

def speak_text(text, lang):
    try:
        filename = f"translated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()
        pygame.mixer.quit()
        time.sleep(1)
        os.remove(filename)
    except Exception as e:
        st.error(f"❌ TTS failed: {e}")

# --- UI Setup ---
st.set_page_config(page_title="🎤 Smart Speech Translator", layout="centered")
st.title("🌐 Smart Speech-to-Speech Translator")
st.markdown("Speak in **any language**, and your words will be **auto-detected**, translated, and spoken out loud.")

# --- Target Language Dropdown ---
unified_languages = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Hindi": "hi",
    "Tamil": "ta",
    "Arabic": "ar",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-cn",
    "Russian": "ru",
    "Italian": "it",
    "Portuguese": "pt",
    "Turkish": "tr",
    "Dutch": "nl"
}

target_name = st.selectbox("🔊 Select your **output language**", list(unified_languages.keys()))
target_lang = unified_languages[target_name]

# --- Loop control checkbox ---
loop_enabled = st.checkbox("✅ Enable continuous translation loop", key="loop_toggle")

if loop_enabled:
    st.info("🎙️ Listening... Will keep going until you uncheck the box.")

    while st.session_state.get("loop_running", True):
        if not st.session_state.get("loop_start", False):
            st.session_state.loop_start = True
            st.success("🔁 Loop started. Speak anytime.")

        with st.spinner("Listening and detecting..."):
            spoken_text = recognize_speech()  # Default to 'en-US' to get the audio

            if spoken_text:
                if len(spoken_text.strip()) < 10:
                    st.warning("⚠️ Input too short to detect language accurately. Defaulting to English.")
                    detected_lang = "en"
                else:
                    try:
                        detected_lang = detect(spoken_text)
                        st.success(f"🧠 Detected Language: {detected_lang.upper()}")
                    except LangDetectException:
                        detected_lang = "en"
                        st.warning("⚠️ Could not detect language. Defaulted to English.")

                translated = translate_text(spoken_text, target_lang)
                if translated:
                    st.success(f"🌍 Translated: {translated}")
                    st.write("🔊 Playing translated audio...")
                    speak_text(translated, target_lang)

        if not st.session_state.get("loop_toggle", False):
            st.warning("🛑 Loop stopped.")
            st.session_state.loop_start = False
            break
