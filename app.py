import streamlit as st
from googletrans import Translator
import openai
import pyttsx3  
from gtts import gTTS
import os

st.set_page_config(page_title="AI Translator", page_icon="🌐", layout="wide")
st.sidebar.title("Translation Settings")

languages = {
    'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de', 
    'Chinese': 'zh-cn', 'Arabic': 'ar', 'Hindi': 'hi', 'Japanese': 'ja'
}

st.sidebar.header("AI Translation Options")
use_ai_translation = st.sidebar.checkbox("Use Advanced AI Translation")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

def main():  
    st.title("🌍 Universal AI Translator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox("Source Language", list(languages.keys()), index=0)
        source_text = st.text_area("Enter text to translate:", height=200)
    
    with col2:
        target_lang = st.selectbox("Target Language", list(languages.keys()), index=1)
        
        translate_btn = st.button("Translate", type="primary")
    
    if translate_btn and source_text:
        translator = Translator()
        translated_text = translator.translate(
            source_text, 
            src=languages[source_lang], 
            dest=languages[target_lang]
        ).text
        
        if use_ai_translation and openai_api_key:
            try:
                openai.api_key = openai_api_key
                ai_translation = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional translator."},
                        {"role": "user", "content": f"Translate from {source_lang} to {target_lang}: {source_text}"}
                    ]
                )
                translated_text = ai_translation.choices[0].message.content
            except Exception as e:
                st.error(f"AI Translation Error: {e}")
        
        st.subheader("Translated Text")
        st.write(translated_text)
        st.sidebar.header("Audio Output")
        audio_option = st.sidebar.selectbox("Select Audio Method", 
                                            ["gTTS (Google)", "pyttsx3 (Local)"])
        
        if st.sidebar.button("Generate Audio"):
            if audio_option == "gTTS (Google)":
                tts = gTTS(text=translated_text, lang=languages[target_lang])
                tts.save("translation.mp3")
                st.audio("translation.mp3")
            else:
                engine = pyttsx3.init()
                engine.save_to_file(translated_text, 'translation_local.mp3')
                engine.runAndWait()
                st.audio("translation_local.mp3")

if __name__ == "__main__":
    main()