import streamlit as st
from llama_index.core.llms import ChatMessage
import logging
import time
from llama_index.llms.ollama import Ollama
from query_data import query_rag

logging.basicConfig(level=logging.INFO)

if 'messages' not in st.session_state:
    st.session_state.messages = []

def stream_chat(model, messages):
    try:
        user_message = messages[-1].content
        context = query_rag(user_message)

        prompt = f"Answer the question based only on the following context:\n\n{context}\n\n---\n\n{user_message}"

        llm = Ollama(model=model, request_timeout=120.0) 
        messages_with_context = [ChatMessage(role='user', content=prompt)]

        resp = llm.stream_chat(messages_with_context)
        response = ""
        response_placeholder = st.empty()

        for r in resp:
            response += r.delta
            response_placeholder.write(response)

        logging.info(f"Model: {model}, Messages: {messages_with_context}, Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        raise e

#main function for streamlit app
def main():
    st.title("Querious")
    logging.info("App started")

    #model selection
    model = "openhermes"
    logging.info(f"Model selected: {model}")

    #prompt user for question
    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        logging.info(f"User input: {prompt}")

        #display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                start_time = time.time()
                logging.info("Generating response")

                with st.spinner("Writing..."):
                    try:
                        messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in st.session_state.messages]
                        response_message = stream_chat(model, messages)
                        duration = time.time() - start_time
                        response_message_with_duration = f"{response_message}\n\nDuration: {duration:.2f} seconds"
                        st.session_state.messages.append({"role": "assistant", "content": response_message_with_duration})
                        logging.info(f"Response: {response_message}")

                    except Exception as e:
                        #error handling
                        st.session_state.messages.append({"role": "assistant", "content": str(e)})
                        st.error("An error occurred while generating the response.")
                        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
