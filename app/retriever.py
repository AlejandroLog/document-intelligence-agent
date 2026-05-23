from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_PATH = "storage/curated/chroma_db"

def get_retriever():
    """
    Se conecta a la base de datos vectorial existente y devuelve un 
    recuperador (retriever) para buscar en los documentos.
    """
    embeddings_model = OpenAIEmbeddings()
    vector_db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings_model
    )
    
    # Configuramos para que devuelva los 3 fragmentos más relevantes
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    return retriever