from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from .brain.agent import brain


APP_NAME = "root_agent"
USER_ID = "user_123"

initial_state = {
    "username": "nihar",
    "interaction_history": []
}


session_service = InMemorySessionService()

runner = Runner(
    agent=brain,
    app_name=APP_NAME,
    session_service=session_service
)


async def create_agent_session():

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state
    )

    return session


async def main_async(
    query: str,
    session_id: str,
    language_code: str
):

    current_turn = f"""
Current user message:
{query}

Detected dominant language:
{language_code}

Important:
The detected language is the dominant language identified by the
speech-to-text system. It does not necessarily mean that the user
wants a monolingual response.

Analyze the actual user message for code-mixing.

If the message is code-mixed, respond naturally in the same
code-mixed style.

If the message is primarily one language, respond in that language.

Always prioritize the language and communication style of the
CURRENT user message rather than previous turns.
"""

    new_message = types.Content(
        role="user",
        parts=[
            types.Part(text=current_turn)
        ]
    )

    final_response = None

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=new_message
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    return final_response