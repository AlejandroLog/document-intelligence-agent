from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import Tool
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.retriever import get_retriever
from app.llm import get_llm

def get_agent():
    llm = get_llm()
    retriever = get_retriever()

    # ---------------- HERRAMIENTAS (TOOLS) ----------------
    def buscar_en_documentos(query):
        documentos = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in documentos])

    tool_rag = Tool(
        name="buscar_documentos",
        func=buscar_en_documentos,
        description="Busca y devuelve información de los documentos procesados. Úsala OBLIGATORIAMENTE cuando el usuario pregunte sobre el contenido de un archivo o texto."
    )

    tool_resumir = Tool(
        name="resumir_conceptos",
        func=lambda x: llm.invoke(f"Resume este concepto brevemente: {x}").content,
        description="Úsala cuando el usuario pida explícitamente un resumen general de un tema."
    )

    tool_entidades = Tool(
        name="extraer_entidades",
        func=lambda x: llm.invoke(f"Extrae en una lista las entidades clave (personas, lugares, fechas, tecnologías) de esta frase: {x}").content,
        description="Úsala si el usuario pide listar entidades importantes, nombres, fechas o lugares."
    )

    tools = [tool_rag, tool_resumir, tool_entidades]

    # ---------------- PROMPT BASE ----------------
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente de investigación inteligente. Tienes acceso a varias herramientas para consultar documentos y extraer información. Úsalas cuando sea necesario."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # ---------------- MEMORIA CONVERSACIONAL ----------------
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # ---------------- INICIALIZAR AGENTE MODERNO ----------------
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        memory=memory,
        handle_parsing_errors=True
    )

    return agent_executor