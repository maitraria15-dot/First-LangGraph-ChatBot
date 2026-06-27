import os
from dotenv import load_dotenv

import streamlit as st

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# --------------------------
# Load Environment Variables
# --------------------------

load_dotenv()

# --------------------------
# Create the LLM
# --------------------------

llm = ChatGroq(
    api_key = os.getenv("GROQ_API_KEY"),
    model = "llama-3.1-8b-instant"

)

# --------------------------
# Define State
# --------------------------

class State(TypedDict):
    messages: Annotated[list, add_messages]

# --------------------------
# Chatbot Node
# --------------------------

def chatbot(state: State):

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }

# --------------------------
# Build Graph
# --------------------------

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()

# -------------------------
# Streamlit UI
# -------------------------

st.title("My First LangGraph Chatbot")

user_input = st.chat_input("Ask me anything ....")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    try:

        result  = graph.invoke(
            {
                "messages": [HumanMessage(content = user_input)]
            }
        )

        reply = result["messages"][-1].content

    except Exception as e:
        reply = str(e)

    with st.chat_message("assistant"):
        st.markdown(reply)