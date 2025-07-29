import sounddevice as sd
from scipy.io.wavfile import write

SAMPLE_RATE = 16000
DURATION = 6  # sekundy

print("Nagrywanie... Powiedz 'cześć sofi'")
audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
sd.wait()
write("wake_test.wav", SAMPLE_RATE, audio)
print("Nagranie zapisane jako wake_test.wav")