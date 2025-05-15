import torch
import numpy as np
from transformers import MusicgenForConditionalGeneration, AutoProcessor
from scipy.io.wavfile import write
from pathlib import Path
import logging
from config import Config


class AudioGenerator:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.logger = logging.getLogger(__name__)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Инициализация модели и процессора
        self.processor = AutoProcessor.from_pretrained(self.cfg.TTA_MODEL)
        self.model = MusicgenForConditionalGeneration.from_pretrained(self.cfg.TTA_MODEL).to(self.device)

    def generate(self, prompt: str, idx: int) -> Path:
        """Генерация высококачественного аудио"""
        try:
            # Подготовка текста
            inputs = self.processor(
                text=[prompt],
                padding=True,
                return_tensors="pt",
            ).to(self.device)

            # Генерация аудио с увеличенной длиной
            audio_values = self.model.generate(
                **inputs,
                max_new_tokens=self.cfg.MAX_NEW_TOKENS,
                do_sample=True,
                temperature=self.cfg.TEMPERATURE
            )

            # Декодирование и обработка аудио
            audio_array = self.processor.batch_decode(audio_values, return_tensors="np")[0]
            audio_array = np.squeeze(audio_array)
            audio_array = np.clip(audio_array, -1.0, 1.0)
            audio_int16 = (audio_array * 32767).astype(np.int16)

            # Сохранение файла
            path = self.cfg.AUDIO_TEMP / f"segment_{idx}.wav"
            write(path, self.cfg.SAMPLE_RATE, audio_int16)

            self.logger.info(f"Audio segment generated: {path}")
            return path

        except Exception as e:
            self.logger.error(f"Generation failed: {str(e)}")
            raise RuntimeError(f"Audio generation error: {str(e)}")