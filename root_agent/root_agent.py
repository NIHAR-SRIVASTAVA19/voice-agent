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


async def main_async(query: str, session_id: str):

    new_message = types.Content(
        role="user",
        parts=[
            types.Part(text=query)
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