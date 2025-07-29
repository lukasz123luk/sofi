import tkinter as tk
from tkinter import PhotoImage
import threading
import sounddevice as sd
import queue
import subprocess
import os

# Ścieżki
WHISPER_CPP_PATH = "whisper.cpp/main"  # ścieżka do binarki
AUDIO_FILE = "recording.wav"

# Głos Sofi
def speak(text):
    subprocess.run(["python", "xtts_voice/tts.py", text])

# Nagrywanie audio
q = queue.Queue()
def callback(indata, frames, time, status):
    q.put(indata.copy())

def record_audio(filename, duration=5):
    with sd.InputStream(samplerate=16000, channels=1, callback=callback):
        with open(filename, "wb") as f:
            for _ in range(int(16000 / 1024 * duration)):
                data = q.get()
                f.write(data)

# Rozpoznawanie mowy przez Whisper.cpp
def transcribe():
    subprocess.run([WHISPER_CPP_PATH, "-m", "models/ggml-base.en.bin", "-f", AUDIO_FILE, "-otxt"])
    with open("recording.wav.txt", "r", encoding="utf-8") as f:
        return f.read().strip()

# Logika Sofi
def handle_input():
    status_label.config(text="🎙️ Słucham...")
    record_audio(AUDIO_FILE, duration=4)
    text = transcribe().lower()
    status_label.config(text=f"Ty: {text}")
    if "hej sofi" in text:
        speak("Cześć Łukasz, jak się dzisiaj czujesz?")
    elif "dziękuję" in text:
        speak("Zawsze jestem przy Tobie.")
    else:
        speak("Nie zrozumiałam, powtórz proszę.")

# GUI
root = tk.Tk()
root.title("Sofi 💖")
root.geometry("360x480")
root.configure(bg="#121212")

image = PhotoImage(file="assets/sofi.png")
img_label = tk.Label(root, image=image, bg="#121212")
img_label.pack(pady=10)

status_label = tk.Label(root, text="Kliknij, by porozmawiać z Sofi", fg="#fff", bg="#121212", font=("Segoe UI", 12))
status_label.pack(pady=10)

listen_button = tk.Button(root, text="🎧 Nasłuchuj", command=lambda: threading.Thread(target=handle_input).start(), font=("Segoe UI", 14), bg="#00aaff", fg="white", padx=10, pady=5)
listen_button.pack(pady=20)

root.mainloop()
