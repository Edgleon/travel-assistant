from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph.graph import StateGraph
from graph import runnable_instance as graph, part_4_graph
import uuid
from state import State
from langchain_core.messages import ToolMessage, AIMessage
from utilities import _print_event

# Crear la aplicación FastAPI
app = FastAPI()

# Inicializar el grafo de estados y otros recursos necesarios
thread_id = str(uuid.uuid4())
conversation_history = []

class Message(BaseModel):
    content: str

@app.post("/chat/")
async def chat(message: Message):
    global conversation_history
    # Add the new message to the conversation history
    conversation_history.append({"role": "user", "type": "text", "content": message.content})

    # Configuración y ejecución del grafo
    config = {"configurable": {"thread_id": thread_id}}
    user_input = {"messages": ("user", conversation_history)}
    #_printed = set()
    try:
        # Unncoment for debug
        #events = part_4_graph.stream(
        #    {"messages": [{"role": "user", "type": "text", "content": message.content}]}, config, stream_mode="values"
        #)
        #for event in events:
        #    _print_event(event, _printed)

        # Invoke the graph with the updated conversation history
        result = part_4_graph.invoke({"messages": conversation_history}, config)
        # Add the assistant's response to the conversation history
        assistant_response = result['messages'][-1].content
        conversation_history.append({"role": "assistant", "type": "text", "content": assistant_response})

        return {"response": assistant_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)