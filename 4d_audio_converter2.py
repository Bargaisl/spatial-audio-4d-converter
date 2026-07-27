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
        self.root.geometry("700x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#120a1c")

        # Стиль
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", foreground="#b967ff", background="#b967ff", troughcolor="#251a35")
        style.configure("TRadiobutton", background="#120a1c", foreground="#e0d6ff", font=("Segoe UI", 10))
        style.configure("TScale", background="#120a1c", troughcolor="#251a35", bordercolor="#251a35")

        self.input_path = tk.StringVar()
        self.output_format = tk.StringVar(value="mp3")
        self.pan_speed = tk.DoubleVar(value=0.3)
        self.intensity = tk.DoubleVar(value=1.0)

        # Заголовок
        tk.Label(
            root,
            text="🌀 4D Spatial Audio Processor",
            font=("Segoe UI", 16, "bold"),
            bg="#120a1c",
            fg="#b967ff"
        ).pack(pady=(15, 5))

        # Выбор файла
        tk.Label(root, text="Выберите аудиофайл:", font=("Segoe UI", 11), bg="#120a1c", fg="#d0c0ff").pack(pady=(10, 4))
        tk.Entry(root, textvariable=self.input_path, width=80, state='readonly', bg="#1e132f", fg="#ffffff", relief="flat", font=("Consolas", 9)).pack()

        tk.Button(
            root,
            text="📁 Открыть",
            command=self.browse_file,
            bg="#2a1a45",
            fg="#b967ff",
            activebackground="#3a2a55",
            activeforeground="#ffffff",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=4
        ).pack(pady=6)

        # Формат
        tk.Label(root, text="Формат выходного файла:", font=("Segoe UI", 10), bg="#120a1c", fg="#c0b0e0").pack(pady=(10, 4))
        fmt_frame = tk.Frame(root, bg="#120a1c")
        fmt_frame.pack()
        tk.Radiobutton(fmt_frame, text="WAV (без потерь)", variable=self.output_format, value="wav", bg="#120a1c", fg="#e0d6ff", selectcolor="#251a35", activebackground="#120a1c", activeforeground="#00f0ff", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(fmt_frame, text="MP3 (320 kbps)", variable=self.output_format, value="mp3", bg="#120a1c", fg="#e0d6ff", selectcolor="#251a35", activebackground="#120a1c", activeforeground="#00f0ff", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=10)

        # Скорость
        tk.Label(root, text="Скорость движения (обороты/сек):", font=("Segoe UI", 10), bg="#120a1c", fg="#c0b0e0").pack(pady=(12, 4))
        speed_scale = tk.Scale(
            root,
            from_=0.02,
            to=2.0,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            length=520,
            variable=self.pan_speed,
            digits=3,
            showvalue=True,
            bg="#120a1c",
            fg="#00f0ff",
            troughcolor="#251a35",
            activebackground="#b967ff",
            highlightthickness=0,
            font=("Segoe UI", 9)
        )
        speed_scale.pack()

        # Интенсивность
        tk.Label(root, text="Интенсивность переключения (0.1 = плавно, 1.0 = норма, 3.0 = резко):", font=("Segoe UI", 10), bg="#120a1c", fg="#c0b0e0").pack(pady=(12, 4))
        intensity_scale = tk.Scale(
            root,
            from_=0.1,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            length=520,
            variable=self.intensity,
            digits=2,
            showvalue=True,
            bg="#120a1c",
            fg="#00f0ff",
            troughcolor="#251a35",
            activebackground="#b967ff",
            highlightthickness=0,
            font=("Segoe UI", 9)
        )
        intensity_scale.pack()

        # Кнопка обработки
        self.process_btn = tk.Button(
            root,
            text="🚀 Создать эффект 'жуки в голове'",
            command=self.start_processing,
            bg="#b967ff",
            fg="#0a0415",
            activebackground="#d080ff",
            activeforeground="#000000",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            padx=20,
            pady=8
        )
        self.process_btn.pack(pady=20)

        # Прогресс
        self.progress = ttk.Progressbar(root, mode='indeterminate', length=500)
        self.progress.pack(fill='x', padx=80)

    def browse_file(self):
        filetypes = [("Аудиофайлы", "*.mp3 *.wav *.ogg *.flac *.m4a")]
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            self.input_path.set(path)

    def start_processing(self):
        if not self.input_path.get():
            messagebox.showwarning("Внимание", "Выберите входной файл!", parent=self.root)
            return
        self.process_btn.config(state='disabled', bg="#5a3a8a")
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

            phase = 2 * np.pi * speed * t
            left_gain = np.abs(np.cos(phase)) ** sharpness
            right_gain = np.abs(np.sin(phase)) ** sharpness

            max_gain = np.maximum(left_gain, right_gain)
            left_gain = np.divide(left_gain, max_gain, out=np.zeros_like(left_gain), where=max_gain != 0)
            right_gain = np.divide(right_gain, max_gain, out=np.zeros_like(right_gain), where=max_gain != 0)

            left_in = samples[:, 0] if audio.channels == 2 else samples
            right_in = samples[:, 1] if audio.channels == 2 else samples

            left_out = left_in * left_gain
            right_out = right_in * right_gain

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

            if fmt == "mp3":
                out_audio.export(output_file, format="mp3", bitrate="320k")
            else:
                out_audio.export(output_file, format="wav")

            self.root.after(0, lambda: messagebox.showinfo("✅ Готово!", f"Файл сохранён:\n{output_file}\n\n🎧 Надень наушники!", parent=self.root))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("❌ Ошибка", f"Не удалось обработать файл:\n{str(e)}", parent=self.root))
        finally:
            self.root.after(0, self.reset_ui)

    def reset_ui(self):
        self.process_btn.config(state='normal', bg="#b967ff")
        self.progress.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Audio4DConverter(root)
    root.mainloop()
