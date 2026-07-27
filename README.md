# Spatial 8D/4D Audio Converter & Panning Tool 🎧🔊

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Supported-red.svg)](https://ffmpeg.org/)

Скрипт цифровой обработки сигналов (DSP) на Python для преобразования обычных аудиозаписей в объемные треки с эффектом пространственного вращения (8D/4D Audio).

---

## ✨ Ключевые возможности

- 🔄 **Динамическое панорамирование:** Вращение звукового поля вокруг слушателя по синусоидальному закону.
- 🏰 **Акустика помещения:** Наложение легкого эффекта объёма и реверберации.
- 🎵 **Поддержка форматов:** Экспорт и импорт WAV, MP3, FLAC через FFmpeg.

---

## 🛠️ Стек технологий

* **Язык:** Python 3.9+
* **DSP & Обработка:** `pydub`, `numpy`, `scipy`, FFmpeg

---

## 🚀 Запуск

```bash
git clone https://github.com/Bargaisl/spatial-audio-4d-converter.git
cd spatial-audio-4d-converter
pip install pydub numpy scipy
python 4d_audio_converter.py
```
