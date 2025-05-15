import unittest
from audio_utils.generator import AudioGenerator
from config import Config


class TestAudioGen(unittest.TestCase):
    def setUp(self):
        self.cfg = Config()
        self.gen = AudioGenerator(self.cfg)

    def test_generation(self):
        audio = self.gen.generate("Тестовый промпт", 0)
        self.assertTrue(Path(audio).exists())