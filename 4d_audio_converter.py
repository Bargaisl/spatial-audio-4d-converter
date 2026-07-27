import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import numpy as np
from pydub import AudioSegment
from pydub.utils import which
import os

if not which("ffmpeg"):
    messagebox.showerror("Ошибка", "FFmpeg не найден! Положите ffmpeg.exe в папку со скриптом.")
    exit(1)

class Audio4DConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("🎧 4D Audio Converter — Жуки в голове")
        self.root.geometry("680x420")
        self.root.resizable(False, False)

        self.input_path = tk.StringVar()
        self.output_format = tk.StringVar(value="mp3")  # по умолчанию MP3
        self.pan_speed = tk.DoubleVar(value=0.6)  # оборотов в секунду
        self.intensity = tk.DoubleVar(value=4.0)   # степень "резкости"

        # UI
        tk.Label(root, text="Выберите аудиофайл:", font=("Arial", 11)).pack(pady=6)
        tk.Entry(root, textvariable=self.input_path, width=80, state='readonly').pack()
        tk.Button(root, text="📁 Открыть", command=self.browse_file).pack(pady=4)

        # Формат вывода
        tk.Label(root, text="Формат выходного файла:", font=("Arial", 10)).pack(pady=(10, 4))
        fmt_frame = tk.Frame(root)
        fmt_frame.pack()
        tk.Radiobutton(fmt_frame, text="WAV (без потерь)", variable=self.output_format, value="wav").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(fmt_frame, text="MP3 (320 kbps)", variable=self.output_format, value="mp3").pack(side=tk.LEFT, padx=10)

        # Скорость
        tk.Label(root, text="Скорость движения (обороты/сек):", font=("Arial", 10)).pack(pady=(10, 4))
        tk.Scale(root, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, length=450, variable=self.pan_speed).pack()

        # Интенсивность ("резкость")
        tk.Label(root, text="Интенсивность эффекта (чем выше — тем резче переключение):", font=("Arial", 10)).pack(pady=(10, 4))
        tk.Scale(root, from_=1.0, to=8.0, resolution=0.5, orient=tk.HORIZONTAL, length=450, variable=self.intensity).pack()

        self.process_btn = tk.Button(
            root,
            text="🚀 Создать эффект 'жуки в голове'",
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.start_processing
        )
        self.process_btn.pack(pady=15)

        self.progress = ttk.Progressbar(root, mode='indeterminate')
        self.progress.pack(fill='x', padx=60)

    def browse_file(self):
        filetypes = [("Аудиофайлы", "*.mp3 *.wav *.ogg *.flac *.m4a")]
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            self.input_path.set(path)

    def start_processing(self):
        if not self.input_path.get():
            messagebox.showwarning("Внимание", "Выберите входной файл!")
            return

        self.process_btn.config(state='disabled')
        self.progress.start()
        thread = threading.Thread(target=self.process_audio, daemon=True)
        thread.start()

    def process_audio(self):
        try:
            input_file = self.input_path.get()
            fmt = self.output_format.get()
            speed = self.pan_speed.get()
            sharpness = self.intensity.get()

            base = os.path.splitext(input_file)[0]
            output_file = f"{base}_4D.{fmt}"

            audio = AudioSegment.from_file(input_file)
            audio = audio.set_channels(2).set_frame_rate(44100)
            samples = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))

            num_samples = len(samples)
            duration = num_samples / audio.frame_rate
            t = np.linspace(0, duration, num_samples)

            # Фаза движения (от 0 до 2π)
            phase = 2 * np.pi * speed * t

            # Очень резкая панорама: почти всё в одном ухе
            # Используем abs(sin) и возводим в степень для "остроты"
            left_gain = np.abs(np.cos(phase)) ** sharpness
            right_gain = np.abs(np.sin(phase)) ** sharpness

            # Нормализуем, чтобы не было перегрузки
            max_gain = np.maximum(left_gain, right_gain)
            left_gain /= max_gain
            right_gain /= max_gain

            left_in = samples[:, 0] if audio.channels == 2 else samples
            right_in = samples[:, 1] if audio.channels == 2 else samples

            left_out = left_in * left_gain
            right_out = right_in * right_gain

            # Нормализация по громкости
            stereo = np.column_stack((left_out, right_out))
            max_val = np.max(np.abs(stereo))
            if max_val > 0:
                stereo /= max_val

            stereo = (stereo * 32767).astype(np.int16)
            out_audio = AudioSegment(
                stereo.tobytes(),
                frame_rate=audio.frame_rate,
                sample_width=2,
                channels=2
            )

            # Экспорт
            if fmt == "mp3":
                out_audio.export(output_file, format="mp3", bitrate="320k")
            else:
                out_audio.export(output_file, format="wav")

            self.root.after(0, lambda: messagebox.showinfo("✅ Готово!", f"Файл сохранён:\n{output_file}\n\n🎧 Надень наушники!"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("❌ Ошибка", f"Не удалось обработать файл:\n{str(e)}"))
        finally:
            self.root.after(0, self.reset_ui)

    def reset_ui(self):
        self.process_btn.config(state='normal')
        self.progress.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Audio4DConverter(root)
    root.mainloop()
