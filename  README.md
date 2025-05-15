# AI Audio Assistant

## Installation
1. Clone repository
2. Install dependencies:
```bash
pip install -r requirements.txt
sudo apt-get install ffmpeg
```
Create .env file with your OpenAI API key:

OPENAI_API_KEY=your_api_key


```run
streamlit run app.py
```


ai-audio-assistant/
│
├── audio_utils/
│   ├── __init__.py
│   ├── generator.py     # Обращение к text to audio
│   ├── merger.py        # Объединение сэмплов в один wav файл
│   └── temp/            # Аудио результаты
│
├── llm/
│   ├── __init__.py
│   ├── advisor.py       # Обращение к llm
│   └── cache/          
│
├── prompts/
│   └── modes.json      # Шаблоны режимов
│
├── config.py           # Централизованная конфигурация
├── app.py              # Streamlit интерфейс
├── requirements.txt    # Зависимости
└── README.md           # Инструкции