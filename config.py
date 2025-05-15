import os
from pathlib import Path
import logging


class Config:
    def __init__(self):
        self.ROOT = Path(__file__).parent.resolve()
        self._setup_paths()
        self._setup_logging()
        self._setup_audio()
        self._setup_models()

    def _setup_paths(self):
        """Инициализация всех путей проекта"""
        self.MODES_PATH = self.ROOT / "prompts" / "modes.json"
        self.AUDIO_TEMP = self.ROOT / "audio_utils" / "temp"
        self.LLM_CACHE = self.ROOT / "llm" / "cache"

        # Создание директорий
        self.AUDIO_TEMP.mkdir(exist_ok=True, parents=True)
        self.LLM_CACHE.mkdir(exist_ok=True, parents=True)

    def _setup_logging(self):
        """Настройка системы логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.ROOT / 'app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _setup_audio(self):
        """Параметры для высококачественного аудио"""
        self.TTA_MODEL = "facebook/musicgen-medium"
        self.SAMPLE_RATE = 32000  # Частота дискретизации
        self.MAX_NEW_TOKENS = 1024  # Длина аудио примерно 20.5 секунд
        self.TEMPERATURE = 0.7  # Креативность генерации
        self.AUDIO_SEGMENTS = 3  # Количество сегментов
        self.CROSSFADE_MS = 3000  # Плавный переход между сегментами примерно 3 секунды

    def _setup_models(self):
        """Параметры моделей ИИ"""
        self.TTA_MODEL = "facebook/musicgen-small"
        self.LLM_MODEL = "gpt-4"
        self.MAX_TOKENS = 256
        self.TEMPERATURE = 0.7

    def clean_temp_files(self):
        """Очистка временных файлов"""
        for file in self.AUDIO_TEMP.glob("*"):
            try:
                if file.is_file():
                    file.unlink()
            except Exception as e:
                self.logger.error(f"Error deleting {file}: {e}")