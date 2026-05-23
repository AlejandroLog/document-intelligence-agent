from app.rag import get_agent

def main():
    print("🤖 Inicializando el Agente RAG...")
    agente = get_agent()
    
    # Pregunta de prueba basada en el documento que subimos en la Fase 3
    pregunta = "¿Qué dice el documento sobre LangChain y MinIO?"
    print(f"\n👤 Usuario: {pregunta}\n")
    
    # Invocamos al agente
    respuesta = agente.invoke({"input": pregunta})
    
    print("\n========================================")
    print(f"🤖 Respuesta final: {respuesta['output']}")
    print("========================================\n")

if __name__ == "__main__":
    main()