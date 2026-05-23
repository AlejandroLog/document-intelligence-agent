import sys
import os

# --- FIX DE RUTAS ---
# Esto le dice a Python que busque módulos en la carpeta raíz (un nivel arriba de 'app')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import tempfile
from minio import Minio
from dotenv import load_dotenv

from pipelines.ingest import upload_to_raw
from pipelines.preprocess import process_and_stage
from pipelines.chunking import chunk_text
from app.embeddings import create_vector_store
from app.rag import get_agent

load_dotenv()

# ... (Todo el resto de tu código de la interfaz se queda exactamente igual hacia abajo)

# Configuración de la página
st.set_page_config(page_title="Plataforma RAG", page_icon="🤖", layout="wide")
st.title("Plataforma RAG para Consulta de Documentos 📄🤖")

# --- 1. INICIALIZAR SESIÓN ---
# Mantenemos el agente y el historial en la memoria de la sesión de Streamlit
if "agent" not in st.session_state:
    st.session_state.agent = get_agent()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Sube un documento en el menú lateral y pregúntame lo que quieras sobre él."}]

# --- 2. BARRA LATERAL (SUBIR ARCHIVOS) ---
with st.sidebar:
    st.header("⚙️ Gestión de Documentos")
    uploaded_file = st.file_uploader("Sube un documento PDF o DOCX", type=["pdf", "docx"])
    
    if uploaded_file and st.button("Procesar Documento"):
        with st.spinner("Ejecutando Pipeline de Datos..."):
            try:
                # 1. Guardar el archivo temporalmente en la PC para que MinIO lo pueda agarrar
                temp_dir = tempfile.mkdtemp()
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 2. Pipeline RAW -> STAGING
                st.info("Subiendo a capa RAW...")
                upload_to_raw(file_path, uploaded_file.name)
                
                st.info("Extrayendo texto a capa STAGING...")
                process_and_stage(uploaded_file.name)
                
                # 3. Descargar texto de STAGING
                st.info("Vectorizando capa CURATED...")
                minio_client = Minio(
                    os.getenv("MINIO_ENDPOINT", "localhost:9000"),
                    access_key=os.getenv("MINIO_ROOT_USER", "admin"),
                    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "password123"),
                    secure=False
                )
                staging_name = f"{os.path.splitext(uploaded_file.name)[0]}.txt"
                response = minio_client.get_object("staging", staging_name)
                texto_completo = response.read().decode('utf-8')
                response.close()
                response.release_conn()
                
                # 4. Chunking y Embeddings
                chunks = chunk_text(texto_completo)
                create_vector_store(chunks, document_name=uploaded_file.name)
                
                # 5. Actualizar el Agente para que reconozca los nuevos datos
                st.session_state.agent = get_agent()
                
                st.success(f"¡El documento '{uploaded_file.name}' está listo para consultas!")
            except Exception as e:
                st.error(f"Ocurrió un error al procesar el archivo: {e}")

# --- 3. ÁREA DE CHAT PRINCIPAL ---
# Mostrar el historial de mensajes
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Capturar la entrada del usuario
if prompt := st.chat_input("¿Qué dice el documento sobre...? o Extrae las entidades de..."):
    # Agregar la pregunta al historial y mostrarla
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("Analizando documentos y pensando..."):
        # Invocamos al Agente RAG
        respuesta = st.session_state.agent.invoke({"input": prompt})
        texto_respuesta = respuesta["output"]
        
        # Guardar respuesta y mostrarla
        st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
        st.chat_message("assistant").write(texto_respuesta)