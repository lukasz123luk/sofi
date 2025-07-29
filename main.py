import tkinter as tk
from threading import Thread
import listener
from speech.tts import speak

is_listening = False

def on_wake():
    speak("Cześć Łukasz, słucham Cię 💗")
    # Tu możesz dodać dalsze rozpoznawanie lub obsługę poleceń

def toggle_listening():
    global is_listening
    if not is_listening:
        is_listening = True
        button.config(text="⏹️ Zatrzymaj nasłuch")
        listener.stop_threads = False
        Thread(target=listener.start_listener, args=(on_wake,), daemon=True).start()
    else:
        is_listening = False
        button.config(text="🎙️ Włącz nasłuch")
        listener.stop_threads = True  # zatrzymanie nasłuchu

root = tk.Tk()
root.title("Sofi GUI")
button = tk.Button(root, text="🎙️ Włącz nasłuch", command=toggle_listening, width=25, height=2)
button.pack(padx=20, pady=20)
root.mainloop()