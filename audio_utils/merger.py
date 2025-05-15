from pydub import AudioSegment
import logging
from pathlib import Path


class AudioMerger:
    def __init__(self, cfg):
        self.cfg = cfg
        self.logger = logging.getLogger(__name__)

    def merge(self, files: list) -> Path:
        """Объединение WAV файлов с сохранением качества"""
        try:
            combined = AudioSegment.empty()

            for i, file_path in enumerate(files):
                segment = AudioSegment.from_wav(file_path)

                if i > 0:
                    combined = combined.append(
                        segment[:self.cfg.CROSSFADE_MS],
                        crossfade=self.cfg.CROSSFADE_MS
                    )
                    combined = combined.append(segment[self.cfg.CROSSFADE_MS:])
                else:
                    combined = segment

            output_path = self.cfg.AUDIO_TEMP / "final_output.wav"
            combined.export(
                output_path,
                format="wav",
                parameters=["-ar", str(self.cfg.SAMPLE_RATE)]
            )

            return output_path

        except Exception as e:
            self.logger.error(f"Merging failed: {str(e)}")
            raise RuntimeError(f"Audio merging error: {str(e)}")