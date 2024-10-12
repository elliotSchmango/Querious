import streamlit as st
from llama_index.core.llms import ChatMessage
import logging
import time
from llama_index.llms.ollama import Ollama
from query_data import query_rag  # Import the RAG function

# Logo work
HRSD_LOGO = "./logo-hrsd.png"
st.logo(HRSD_LOGO)

logging.basicConfig(level=logging.INFO)

# Initialize chat history in session state if not already present
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to stream chat response based on selected model and retrieved context
def stream_chat(model, messages):
    try:
        # Get the user's query from the chat history
        user_message = messages[-1].content  # Assuming the user's last message is the query

        # Use RAG to fetch relevant context from the Chroma database
        context = query_rag(user_message)  # Call query_rag to get relevant context based on the query

        # Combine the retrieved context and user message into a single prompt
        prompt = f"Answer the question based only on the following context:\n\n{context}\n\n---\n\n{user_message}"

        # Initialize the language model with a timeout and pass the prompt with context
        llm = Ollama(model=model, request_timeout=120.0) 
        messages_with_context = [ChatMessage(role='user', content=prompt)]

        # Stream chat responses from the model
        resp = llm.stream_chat(messages_with_context)
        response = ""
        response_placeholder = st.empty()

        # Append each piece of the response to the output
        for r in resp:
            response += r.delta
            response_placeholder.write(response)

        # Log the interaction details
        logging.info(f"Model: {model}, Messages: {messages_with_context}, Response: {response}")
        return response
    except Exception as e:
        # Log and re-raise any errors that occur
        logging.error(f"Error during streaming: {str(e)}")
        raise e

# Main function for the Streamlit app
def main():
    st.title("HRSD LLM")  # Set the title of the Streamlit app
    logging.info("App started")  # Log that the app has started

    # Sidebar for model selection
    model = "openhermes"
    logging.info(f"Model selected: {model}")

    # Prompt for user input and save to chat history
    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        logging.info(f"User input: {prompt}")

        # Display the user's query
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Generate a new response if the last message is not from the assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                start_time = time.time()  # Start timing the response generation
                logging.info("Generating response")

                with st.spinner("Writing..."):
                    try:
                        # Prepare messages for the LLM and stream the response
                        messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in st.session_state.messages]
                        response_message = stream_chat(model, messages)  # Call the modified stream_chat
                        duration = time.time() - start_time  # Calculate the duration
                        response_message_with_duration = f"{response_message}\n\nDuration: {duration:.2f} seconds"
                        st.session_state.messages.append({"role": "assistant", "content": response_message_with_duration})
                        logging.info(f"Response: {response_message}")

                    except Exception as e:
                        # Handle errors and display an error message
                        st.session_state.messages.append({"role": "assistant", "content": str(e)})
                        st.error("An error occurred while generating the response.")
                        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
