from datetime import datetime
import streamlit as st
import asyncio
import json
import uuid

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from runnable import get_runnable


@st.cache_resource
def create_chatbot_instance():
    return get_runnable()


chatbot = create_chatbot_instance()


@st.cache_resource
def get_thread_id():
    return str(uuid.uuid4())


thread_id = get_thread_id()

system_message = f"""
        You are a AI assistant who is an expert in hairloss.
        You can access the users hairloss name, condition, age, medications, allergies etc. using tools.
        You can provide information about hairloss based on the user's data.
        Use only given information do not make up any information. Current date is {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.
    """


async def prompt_ai(messages):
    config = {"configurable": {"thread_id": thread_id}}

    async for event in chatbot.astream_events(
        {"messages": messages}, config, version="v2"
    ):
        if event["event"] == "on_chat_model_stream":
            yield event["data"]["chunk"].content


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


async def main():
    st.title("CokGuzelYasa Chatbot")

    # Initialize chat with an introduction message
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=system_message),
            AIMessage(
                content="Hello! I am CokGuzelYasa Chatbot. How can I help you today?"
            ),
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        message_json = json.loads(message.model_dump_json())
        message_type = message_json["type"]
        if message_type in ["human", "ai"]:  # exclude system messages
            with st.chat_message(message_type):
                st.markdown(message_json["content"])

    # React to user input
    if prompt := st.chat_input("What would you like to do today?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(content=prompt))

        # Display assistant response in chat message container
        response_content = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()  # Placeholder for updating the message
            # Run the async generator to fetch responses (this part enables the streaming)
            async for chunk in prompt_ai(st.session_state.messages):
                response_content += chunk

                # Update the placeholder with the current response content
                message_placeholder.markdown(response_content)

        st.session_state.messages.append(AIMessage(content=response_content))


if __name__ == "__main__":
    asyncio.run(main())
