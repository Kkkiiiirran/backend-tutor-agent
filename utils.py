from datetime import datetime

from google.genai import types

from datetime import datetime

async def update_interaction_history(session_service, app_name, user_id, session_id, entry):
    """Add an entry (dict) to the interaction history in session state."""
    try:
        # Fetch current session
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        interaction_history = session.state.get("history", [])

        # Ensure entry is dict with required keys and timestamp
        if not isinstance(entry, dict):
            raise ValueError("History entry must be a dictionary")
        if "action" not in entry:
            raise ValueError("History entry must have 'action' key")
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        interaction_history.append(entry)

        # Update session state
        updated_state = session.state.copy()
        updated_state["history"] = interaction_history

        # Save updated session state
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=updated_state,
        )
    except Exception as e:
        print(f"Error updating interaction history: {e}")


async def add_user_query_to_history(session_service, app_name, user_id, session_id, query):
    """Add a user query string wrapped in a dict to the history."""
    await update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "user_query",
            "query": query,
        },
    )



async def add_agent_response_to_history(session_service, app_name, user_id, session_id, agent_name, response):
    """Add an agent response string wrapped in a dict to the history."""
    await update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "agent_response",
            "agent": agent_name,
            "response": response,
        },
    )

async def display_state(session_service, app_name, user_id, session_id, label="Current State"):
    """Print the current tutor session state in readable format."""
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        print(f"\n{'-' * 10} {label} {'-' * 10}")

        user_name = session.state.get("user_name", "Unknown")
        print(f"👤 User: {user_name}")

        history = session.state.get("history", [])
        if history:
            print("📖 Interaction History:")
            for idx, item in enumerate(history, 1):
                if isinstance(item, dict):
                    action = item.get("action", "unknown")
                    if action == "user_query":
                        print(f"  {idx}. User: {item.get('query', '')}")
                    elif action == "agent_response":
                        print(f"  {idx}. {item.get('agent', 'Agent')}: {item.get('response', '')}")
                    else:
                        # Unknown action fallback
                        print(f"  {idx}. {action}: {item}")
                else:
                    # Non-dict fallback
                    print(f"  {idx}. {item}")
        else:
            print("📖 Interaction History: None")



        print("-" * (22 + len(label)))
    except Exception as e:
        print(f"Error displaying state: {e}")


async def process_agent_response(event):
    """Extract and return the final tutor response text."""
    final_response = None
    if event.is_final_response():
        if (
            event.content and
            event.content.parts and
            hasattr(event.content.parts[0], "text") and
            event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None
    agent_name = None

    # Display state before processing the message
    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
    )

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # Capture the agent name from the event if available
            if event.author:
                agent_name = event.author

            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        # print(f"{Colors.BG_RED}{Colors.WHITE}ERROR during agent run: {e}{Colors.RESET}")
        pass

    # Add the agent response to interaction history if we got a final response
    if final_response_text and agent_name:
        await add_agent_response_to_history(
            runner.session_service,
            runner.app_name,
            user_id,
            session_id,
            agent_name,
            final_response_text,
        )

    # Display state after processing the message
    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State AFTER processing",
    )

    # print(f"{Colors.YELLOW}{'-' * 30}{Colors.RESET}")
    return final_response_text