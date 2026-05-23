






from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Divide un texto largo en fragmentos más pequeños (chunks).
    - chunk_size: Cantidad máxima de caracteres por fragmento.
    - chunk_overlap: Caracteres que se repiten entre un chunk y el siguiente para no perder contexto.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    return chunks