from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from langgraph.graph import StateGraph
from graph import runnable_instance as graph, part_4_graph
import uuid
from state import State
from langchain_core.messages import ToolMessage, AIMessage
from utilities import _print_event
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las fuentes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Inicializar el grafo de estados y otros recursos necesarios
thread_id = str(uuid.uuid4())
conversation_history = []
sessions = {}

class Message(BaseModel):
    content: str

# @app.post("/chat/")
# async def chat(message: Message):
#     global conversation_history
#     # Add the new message to the conversation history
#     conversation_history.append({"role": "user", "type": "text", "content": message.content})

#     # Configuración y ejecución del grafo
#     config = {"configurable": {"thread_id": thread_id}}
#     user_input = {"messages": ("user", conversation_history)}
#     _printed = set()
#     try:
#         # Unncoment for debug
#         events = part_4_graph.stream(
#             {"messages": [{"role": "user", "type": "text", "content": message.content}]}, config, stream_mode="values"
#         )
#         for event in events:
#             _print_event(event, _printed)

#         # Invoke the graph with the updated conversation history
#         result = part_4_graph.invoke({"messages": conversation_history}, config)
#         # Add the assistant's response to the conversation history
#         assistant_response = result['messages'][-1].content
#         conversation_history.append({"role": "assistant", "type": "text", "content": assistant_response})

#         return {"response": assistant_response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    # Crear un identificador único para cada sesión
    thread_id = str(uuid.uuid4())
    # Inicializar la configuración del grafo para esta sesión
    builder = StateGraph(State)
    graph = builder.compile()
    config = {"configurable": {"thread_id": thread_id}}
    conversation_history = []

    # Guardar la configuración del grafo y la historia de la conversación para la sesión
    sessions[thread_id] = {"graph": part_4_graph, "config": config, "conversation_history": conversation_history}

    try:
        while True:
            # Recibir el mensaje del usuario a través del WebSocket
            data = await websocket.receive_text()

            # Añadir el mensaje del usuario al historial de conversación
            conversation_history.append({"role": "user", "type": "text", "content": data})

            # Configuración y ejecución del grafo
            user_input = {"messages": ("user", conversation_history)}
            _printed = set()

            try:
                # Unncoment for debug
                events = part_4_graph.stream(
                    {"messages": [{"role": "user", "type": "text", "content": data}]}, config, stream_mode="values"
                )
                for event in events:
                    _print_event(event, _printed)

                # Ejecución del grafo con el historial de la conversación
                result = part_4_graph.invoke({"messages": conversation_history}, config)

                # Añadir la respuesta del asistente al historial de la conversación
                assistant_response = result['messages'][-1].content
                conversation_history.append({"role": "assistant", "type": "text", "content": assistant_response})

                # Enviar la respuesta al usuario a través del WebSocket
                await websocket.send_text(assistant_response)

            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}")
    except Exception as e:
        await websocket.close()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8100)