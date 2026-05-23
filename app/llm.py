from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """
    Inicializa el modelo de lenguaje principal.
    Usamos temperatura 0 para que sea preciso y no alucine datos.
    """
    return ChatOpenAI(
        model="gpt-3.5-turbo", 
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )