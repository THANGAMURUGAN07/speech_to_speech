Sample output:
![image](https://github.com/user-attachments/assets/2a3ebb5e-1cc4-4b7b-8c1f-dfa2f95af7ff)


🗣️ Smart Speech-to-Speech Translator

A real-time, multilingual voice translator that listens to spoken language, auto-detects the source language, translates it into a selected target language, and speaks the result aloud. Built with Streamlit, Google Translate, and gTTS, this application provides a simple interface for live speech translation.

🔧 Features

🎤 Speech Recognition: Converts microphone input to text using Google's speech recognition.

🧠 Automatic Language Detection: Detects the language of the spoken text using langdetect.

🌐 Translation: Translates the detected speech into your selected target language with googletrans.

🔊 Text-to-Speech: Uses gTTS to vocalize the translated result.

🔁 Continuous Mode: Option to run the translator in a continuous listening loop.

✅ Streamlit Interface: Simple, interactive interface with real-time feedback and emoji indicators.

📦 Requirements

streamlit
pygame
gtts
googletrans==4.0.0-rc1
SpeechRecognition
pyaudio
langdetect

