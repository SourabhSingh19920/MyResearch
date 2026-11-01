import streamlit as st
from langchain_ollama import OllamaLLM
from src.tool import SearchTool
import time

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

@st.cache_resource
def get_search_tool():
    return SearchTool()


llm = get_llm_model()
search_tool = get_search_tool()

# Initializing the side bar for extra options
with st.sidebar:
    model = st.selectbox("LLM Model",["qwen2.5-coder:7b","qwen3-vl:8b","gemma4:e2b"])
    temperature = st.slider("Temperature",max_value=1.0,min_value=0.1,value=0.1)
    duckduckgo_search = st.checkbox("DuckDuckGo Search",value=False)
    wikipedia_search = st.checkbox("Wikipedia Search",value=False)
    

    if st.button("Clear Session"):
        st.session_state.conversation.clear()
        st.rerun()

# Laying out the content of the previous conversation
for message in st.session_state.conversation:
    if message["role"] == "human":
        st.chat_message("human").write(message["content"])
    if message["role"] == "ai":
        st.chat_message("ai").write(message["content"])
        if "duckduckgo_search_result" in message.keys():
            with st.expander("DuckDuckGo Result"):
                for key,value in message["duckduckgo_search_result"].items():
                    st.write(f"{key} : {value}")
        if "wikipedia_search_result" in message.keys():
            with st.expander("Wikipedia Result"):
                for key,value in message["wikipedia_search_result"].items():
                    st.write(f"{key} : {value}")

# Main block of code that will run the main bussiness logic
query = st.chat_input(placeholder="Your query will go here..",accept_audio=True,accept_file=True)
if query:
    st.session_state.conversation.append({"role":"human","content":query.text})
    st.chat_message("human").write(query.text)
    with st.spinner("Thinking...."):
        result_dict = dict()
        response = st.chat_message("ai").write_stream(llm.stream(query.text))
        result_dict = {"role":"ai","content":response}

        if duckduckgo_search:
            search_result_dict = dict()
            with st.expander("Duck Duck Go Search Result"):
                with st.spinner(f"Perfomring DuckDuckGo Search"):
                    search_result = search_tool.duckduckgoSearch(query.text)
                    for result in search_result:
                        for key,value in result.items():
                            search_result_dict[key] = value
                            st.write(f"{key} : {value}")
            result_dict["duckduckgo_search_result"] = search_result_dict

        if wikipedia_search:
            search_result_dict = dict()
            with st.expander("Wikipedia Search Result"):
                with st.spinner(f"Performing Wikipedia Search"):
                    search_result = search_tool.wikipediaSearch(query=query.text)
                    if search_result is not None:
                        st.write(f"Page : {search_result['page']}")
                        st.write(f"Summary : {search_result['summary']}")
                        search_result_dict["Page"] = search_result["page"]
                        search_result_dict["Summary"] = search_result["summary"]
                    else:
                        search_result_dict["result"] = "No Result Found"
            result_dict["wikipedia_search_result"] = search_result_dict
        st.session_state.conversation.append(result_dict)
    st.rerun()




