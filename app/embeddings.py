"""
Módulo de Vectorización curated
Recibe los fragmentos de texto los convierte en 
representaciones matemáticas embeddings consumiendo la API de OpenAI, y 
los guarda de forma persistente en una base de datos vectorial ChromaDB
"""
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Aquí es donde vivirá nuestro índice vectorial (nuestra capa CURATED local)
CHROMA_PATH = "storage/curated/chroma_db"

def create_vector_store(chunks: list, document_name: str):
    """
    Genera embeddings para una lista de fragmentos y los guarda en ChromaDB.
    """
    print(f"Generando embeddings para {len(chunks)} fragmentos usando OpenAI...")
    
    # 1. Inicializar el modelo de embeddings
    # (Asegúrate de tener OPENAI_API_KEY en tu archivo .env)
    embeddings_model = OpenAIEmbeddings()
    
    # 2. Crear metadata para cada chunk (muy útil para saber de qué archivo vino)
    metadatas = [{"source": document_name, "chunk_index": i} for i in range(len(chunks))]
    
    # 3. Insertar en la base de datos vectorial
    vector_db = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings_model,
        metadatas=metadatas,
        persist_directory=CHROMA_PATH
    )
    
    print(f" Embeddings creados y guardados exitosamente en '{CHROMA_PATH}'.")
    return vector_db