import os
from sarvamai.play import play, save
from dotenv import load_dotenv
from sarvamai import SarvamAI


load_dotenv()

client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY")
)

def text_to_speech(
    text: str,
    language: str,
    speaker: str = "shubh"
):
    response = client.text_to_speech.convert(
        model="bulbul:v3",
        text=text,
        language_code=language,
        speaker=speaker,
    )
    save(response, "output.wav")
    play(response)

    return response