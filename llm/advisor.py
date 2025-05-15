import json
from pathlib import Path
import logging
from openai import OpenAI
import os
from dotenv import load_dotenv
from config import Config

load_dotenv()


class LLMAdvisor:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.logger = logging.getLogger(__name__)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_tips(self, mode: str) -> list:
        """Генерация музыкальных подсказок"""
        cache_file = self.cfg.LLM_CACHE / f"{mode}.json"

        # Попытка загрузки из кэша
        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Cache load failed: {e}")

        # Генерация новых подсказок
        try:
            with open(self.cfg.MODES_PATH) as f:
                modes = json.load(f)
                base_prompt = modes[mode]["default_prompt"]

            response = self.client.chat.completions.create(
                model=self.cfg.LLM_MODEL,
                messages=[{
                    "role": "system",
                    "content": f"Generate 5 creative music prompts based on: {base_prompt}"
                }],
                temperature=1.2
            )

            tips = [choice.message.content for choice in response.choices]

            # Сохранение в кэш
            with open(cache_file, "w") as f:
                json.dump(tips, f)

            return tips

        except Exception as e:
            self.logger.error(f"OpenAI error: {str(e)}")
            return [base_prompt]