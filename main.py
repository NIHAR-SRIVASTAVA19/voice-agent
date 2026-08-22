import asyncio
from stt import record_audio, transcribe_audio
from tts import text_to_speech
from root_agent.root_agent import (
    main_async,
    create_agent_session
)
import numpy as np
import sounddevice as sd

async def main():

    session = await create_agent_session()

    print("---------- Voice agent started ----------")
    print("Say 'exit' to end the conversation.")

    while True:

        print("\n---------- Listening to your voice input ----------")

        try:
            audio_path = record_audio()
            stt_result = transcribe_audio(audio_path)
        except Exception as e:
            print("---------- STT failed ----------")
            print(e)
            continue

        print("---------- Your voice input is transcribed to text ----------")
        print("You said:", stt_result.transcript)
        print("Language:", stt_result.language_code)
        print("Language confidence:", stt_result.language_probability)

        if stt_result.transcript.lower().strip() == "exit":
            print("Exiting the voice agent. Goodbye!")
            break

        try:
            llm_response = await main_async(
                stt_result.transcript,
                session.id,
                stt_result.language_code
            )
        except Exception as e:
            print("---------- LLM call failed ----------")
            print(e)
            continue

        print("---------- LLM response ----------")
        print("LLM response:", llm_response)

        try:
            text_to_speech(
            llm_response,
            language=stt_result.language_code
            )
        except Exception as e:
            print("---------- TTS call failed ----------")
            print(e)


if __name__ == "__main__":
    asyncio.run(main())