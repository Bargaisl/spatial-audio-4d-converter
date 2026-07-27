# Spatial 8D/4D Audio Converter & Panning Tool 🎧🔊

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Supported-red.svg)](https://ffmpeg.org/)

---

## English Version

### Description
Digital Signal Processing (DSP) Python script for converting standard audio tracks into spatial 8D/4D audio with dynamic soundstage panning and room acoustics.

### Key Features
- 🔄 **Dynamic Panning:** Rotating sound sources around the listener via sinusoidal algorithms.
- 🏰 **Room Acoustics:** Applying subtle room reverb and space volume.
- 🎵 **Format Support:** Processing WAV, MP3, FLAC via FFmpeg integration.

### Tech Stack
* **Language:** Python 3.9+
* **DSP & Processing:** `pydub`, `numpy`, `scipy`, FFmpeg

### Quick Start
```bash
git clone https://github.com/Bargaisl/audio-4d-conv.git
cd audio-4d-conv
pip install pydub numpy scipy
python 4d_audio_converter.py
```

### ⚠️ Disclaimer & Precautions
This audio conversion tool is provided "as is". Converting high-volume audio signals may cause clipping, distortion, or temporary hearing discomfort if listened to at excessive volumes with headphones. The developer is not liable for hardware damage or hearing damage caused by improper volume levels or corrupted output files.

### License
Licensed under the [MIT License](LICENSE).

---

## Русская версия (Russian Version)

### Описание
Скрипт цифровой обработки сигналов (DSP) на Python для преобразования обычных аудиозаписей в объемные треки с эффектом пространственного вращения (8D/4D Audio).

### Ключевые возможности
- 🔄 **Динамическое панорамирование:** Вращение звукового поля вокруг слушателя по синусоидальному закону.
- 🏰 **Акустика помещения:** Наложение легкого эффекта объёма и реверберации.
- 🎵 **Поддержка форматов:** Экспорт и импорт WAV, MP3, FLAC через FFmpeg.

### Стек технологий
* **Язык:** Python 3.9+
* **DSP & Обработка:** `pydub`, `numpy`, `scipy`, FFmpeg

### Запуск
```bash
git clone https://github.com/Bargaisl/audio-4d-conv.git
cd audio-4d-conv
pip install pydub numpy scipy
python 4d_audio_converter.py
```

### ⚠️ Предупреждение и отказ от ответственности
Данный инструмент обработки аудио предоставляется по принципу «как есть». Преобразование аудиосигналов высокой громкости может вызывать клиппинг, искажения или временный дискомфорт для слуха при прослушивании на чрезмерной громкости в наушниках. Разработчик не несет ответственности за повреждение оборудования или слуха, вызванное ненадлежащим уровнем громкости или поврежденными итоговыми файлами.

### Лицензия
Распространяется под лицензией [MIT License](LICENSE).
