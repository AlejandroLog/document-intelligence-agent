import os
from minio import Minio
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Configurar el cliente de MinIO
minio_client = Minio(
    os.getenv("MINIO_ENDPOINT", "localhost:9000"),
    access_key=os.getenv("MINIO_ROOT_USER", "admin"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "password123"),
    secure=False # Como estamos en localhost, no usamos HTTPS
)

def upload_to_raw(file_path: str, object_name: str) -> bool:
    """
    Sube un documento físico desde tu computadora al bucket 'raw' del Data Lake.
    """
    try:
        minio_client.fput_object(
            "raw",          # Nombre del bucket
            object_name,    # Cómo se llamará en MinIO (ej. "manual.pdf")
            file_path       # Ruta del archivo en tu PC
        )
        print(f"✅ Archivo '{object_name}' subido exitosamente a la capa RAW.")
        return True
    except Exception as e:
        print(f"❌ Error al subir '{object_name}': {e}")
        return False