import streamlit as st
from config import Config
from audio_utils.generator import AudioGenerator
from audio_utils.merger import AudioMerger
from llm.advisor import LLMAdvisor
import json

# Инициализация
cfg = Config()
advisor = LLMAdvisor(cfg)
generator = AudioGenerator(cfg)
merger = AudioMerger(cfg)

# Загрузка режимов
with open(cfg.MODES_PATH, 'r') as f:
    MODES = json.load(f)

# Интерфейс
st.title("🎵 Word2Waves")
mode = st.selectbox("Select mode", list(MODES.keys()))
tips = advisor.get_tips(mode)

# Добавление возможности пользователю ввести свой собственный пропт
use_custom_prompt = st.checkbox("Enter your own prompt")
if use_custom_prompt:
    selected = st.text_area("Write your custom prompt:")
else:
    selected = st.radio("Choose prompt", tips)

if st.button("Generate"):
    cfg.clean_temp_files()

    with st.spinner("Creating high quality audio..."):
        try:
            # Генерация сегментов
            segments = [generator.generate(selected, i) for i in range(cfg.AUDIO_SEGMENTS)]

            # Объединение
            final = merger.merge(segments)

            st.success("High quality audio generated!")
            st.audio(str(final))

            # Кнопка скачивания
            with open(final, 'rb') as f:
                st.download_button(
                    "Download WAV",
                    data=f,
                    file_name="composition.wav",
                    mime="audio/wav"
                )

        except Exception as e:
            st.error(f"Generation error: {str(e)}")
