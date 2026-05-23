import os
import io
from pypdf import PdfReader
import docx
from minio import Minio
from dotenv import load_dotenv

load_dotenv()

minio_client = Minio(
    os.getenv("MINIO_ENDPOINT", "localhost:9000"),
    access_key=os.getenv("MINIO_ROOT_USER", "admin"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "password123"),
    secure=False
)

def extract_text_from_pdf(file_stream) -> str:
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        # Extraer texto de cada página y añadir un salto de línea
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_stream) -> str:
    doc = docx.Document(file_stream)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def process_and_stage(object_name: str):
    """
    Descarga el archivo de RAW, detecta su tipo, extrae el texto
    y guarda el resultado en STAGING como .txt
    """
    response = None
    try:
        print(f"Procesando '{object_name}'...")
        # 1. Obtener el archivo desde el bucket RAW
        response = minio_client.get_object("raw", object_name)
        file_stream = io.BytesIO(response.read())
        
        # 2. Extraer el texto según la extensión del archivo
        texto_extraido = ""
        if object_name.lower().endswith('.pdf'):
            texto_extraido = extract_text_from_pdf(file_stream)
        elif object_name.lower().endswith('.docx'):
            texto_extraido = extract_text_from_docx(file_stream)
        else:
            print(f" Formato no soportado para: {object_name}")
            return

        # 3. Preparar el texto para subirlo a STAGING
        staging_name = f"{os.path.splitext(object_name)[0]}.txt"
        text_bytes = texto_extraido.encode('utf-8')
        text_stream = io.BytesIO(text_bytes)
        
        # 4. Subir el archivo .txt al bucket STAGING
        minio_client.put_object(
            "staging",
            staging_name,
            text_stream,
            length=len(text_bytes)
        )
        print(f"✅ Texto extraído y guardado en la capa STAGING como '{staging_name}'.")

    except Exception as e:
        print(f" Error al procesar '{object_name}': {e}")
    finally:
        if response:
            response.close()
            response.release_conn()