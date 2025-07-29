import os
import sounddevice as sd
import scipy.io.wavfile as wav
import time
import subprocess

# 🎤 Ustaw tu swój mikrofon!
DEVICE_INDEX = 12  # Możesz zmienić na 15, 6 albo 1 jeśli ten nie działa
from pydub import AudioSegment
def record_audio(filename, duration=3, samplerate=44100):
    print("🎙️ Nagrywam...")
    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype='int16',
        device=DEVICE_INDEX
    )
    sd.wait()
    temp_wav = "temp_original.wav"
    wav.write(temp_wav, samplerate, recording)

    print("🔄 Konwertuję do 16kHz...")
    audio = AudioSegment.from_wav(temp_wav)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(filename, format="wav")
    os.remove(temp_wav)
    print("✅ Zapisano:", filename)

    

def transcribe_audio(path_to_wav):
    command = [
        "C:\\Users\\lukil\\Desktop\\Sofi\\whisper.cpp\\main.exe",
        "-m", "models/ggml-small.bin",
        "-f", path_to_wav,
        "-otxt"
    ]
    print("🔍 Rozpoznaję...")
    subprocess.run(command)
    txt_path = path_to_wav.replace('.wav', '.txt')
    if os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return ""

def main_loop():
    print("🔄 Nasłuchiwanie 'Hej Sofi'...")
    while True:
        filename = "sofi_temp.wav"
        record_audio(filename, duration=3)
        text = transcribe_audio(filename)
        print("📄 Rozpoznano:", text)
        if "hej sofi" in text.lower():
            print("💖 Hasło wykryte! Sofi się budzi!")
            break
        time.sleep(1)

if __name__ == "__main__":
    main_loop()
