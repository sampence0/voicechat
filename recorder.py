import pyaudio
import wave
import threading

# Parameters for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def record_audio(output_file="output.wav"):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    def _record():
        nonlocal frames
        while recording:
            data = stream.read(CHUNK)
            frames.append(data)

    global recording
    recording = True

    # Start a new thread for recording audio
    record_thread = threading.Thread(target=_record)
    record_thread.start()

    return frames

def stop_recording(frames, output_file="output.wav"):
    global recording
    recording = False

    audio = pyaudio.PyAudio()

    print("Finished recording.")

    # Save the recorded audio to a .wav file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

