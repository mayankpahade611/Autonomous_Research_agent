from langchain_groq import ChatGroq
import os

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
    return _llm
