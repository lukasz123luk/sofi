import os
import sounddevice as sd
from scipy.io.wavfile import write
import subprocess
import uuid

WHISPER_PATH = "C:\Users\lukil\Desktop\Sofi\whisper.cpp"
MODEL_PATH = os.path.join(WHISPER_PATH, "models", "ggml-base.bin")
MAIN_EXE = os.path.join(WHISPER_PATH, "build", "Release", "main.exe")  # lub "build/main.exe"

def record_audio(filename="input.wav", duration=5, samplerate=16000):
    print("🎤 Nagrywanie...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    write(filename, samplerate, recording)
    print("✅ Nagrano!")

def transcribe_whisper(wav_path="input.wav"):
    temp_output = f"trans_{uuid.uuid4().hex}.txt"
    command = [
        MAIN_EXE,
        "-m", MODEL_PATH,
        "-f", wav_path,
        "-of", temp_output,
        "--output-txt"
    ]
    subprocess.run(command, cwd=WHISPER_PATH)
    
    txt_path = os.path.join(WHISPER_PATH, f"{temp_output}.txt")
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()
        os.remove(txt_path)
        return text.strip()
    return "Nie udało się rozpoznać głosu."

# Test:
if __name__ == "__main__":
    record_audio(duration=5)
    tekst = transcribe_whisper()
    print("🗣️ Sofi zrozumiała:", tekst)
