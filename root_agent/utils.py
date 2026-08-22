async def update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        query
        ):
    session= await session_service.get_session(
        app_name=app_name,
        session_id=session_id,
        user_id=user_id
        )

    if session is  None:
        return "No Session Found"

    interaction_history= session.state.get("interaction_history", [])

    interaction_history.append(query)
    session.state["interaction_history"] = interaction_history