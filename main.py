import streamlit as st
from langchain_ollama import OllamaLLM

# Setting up the streamlit environment
st.set_page_config(layout='wide',page_title="Researcher")
st.title("Web Researcher")


# Initializing the session variables
if "conversation" not in st.session_state:
    st.session_state.conversation = list()


# Caching required chunk of data and models
@st.cache_resource
def get_llm_model() -> OllamaLLM:
    return OllamaLLM(model="qwen2.5-coder:7b",temperature=0.1,reasoning=False)


llm = get_llm_model()

# Initializing the side bar for extra options
with st.sidebar:
    model = st.selectbox("LLM Model",["qwen2.5-coder:7b","qwen3-vl:8b","gemma4:e2b"])
    temperature = st.slider("Temperature",max_value=1.0,min_value=0.1,value=0.1)

    if st.button("Clear Session"):
        st.session_state.conversation.clear()
        st.rerun()

# Laying out the content of the previous conversation
for message in st.session_state.conversation:
    if message["role"] == "human":
        st.chat_message("human").write(message["content"])
    if message["role"] == "ai":
        st.chat_message("ai").write(message["content"])

# Main block of code that will run the main bussiness logic
query = st.chat_input(placeholder="Your query will go here..",accept_audio=True,accept_file=True)
if query:
    st.session_state.conversation.append({"role":"human","content":query.text})
    st.chat_message("human").write(query.text)
    with st.spinner("Thinking...."):
        response = st.chat_message("ai").write_stream(llm.stream(query.text))
        st.session_state.conversation.append({"role":"ai","content":response})
    st.rerun()




