import os
import wave
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from sarvamai import SarvamAI
from dataclasses import dataclass


@dataclass
class TranscriptionResult:
    transcript: str
    language_code: str
    language_probability: float
    request_id: str


load_dotenv()

client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY")
)

SAMPLE_RATE = 16000


def record_audio(path: str = "mic_input.wav") -> str:
    input("Press Enter to start recording...")

    frames = []

    def callback(indata, frame_count, time_info, status):
        frames.append(indata.copy())

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE, channels=1, dtype="int16", callback=callback
    )
    with stream:
        input("Recording... press Enter to stop.")

    audio = np.concatenate(frames, axis=0)

    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

    return path


def transcribe_audio(audio_path: str) -> TranscriptionResult:
    with open(audio_path, "rb") as audio_file:
        response = client.speech_to_text.transcribe(
            file=audio_file,
            model="saaras:v3",            # Specify the Saaras v3 model
            language_code="unknown",      # Tells Saaras to auto-detect the base language
            mode="codemix",               # Keeps English in English script & Indic text in native script
            with_timestamps=True          # Optional: returns time boundaries for words
        )
        return TranscriptionResult(
        transcript=response.transcript,
        language_code=response.language_code,
        language_probability=response.language_probability,
        request_id=response.request_id
    )


if __name__ == "__main__":
    audio_path = record_audio()
    speech_text = transcribe_audio(audio_path)
    print("Transcribed text:", speech_text)