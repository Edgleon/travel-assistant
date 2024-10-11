from assistants.hotel_booking import hotel_booking_assistant
from assistants.excursion_booking import excursion_assistant
from tools.hotel_tools import get_availability_for_hotels
from tools.excursion_tools import get_availability_for_excursions
from langchain_core.runnables import RunnableConfig
from state import State
from assistants.primary import primary_assistant


from dotenv import load_dotenv
load_dotenv()
from typing import List, Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.pydantic_v1 import BaseModel
from langserve import add_routes
import uvicorn
import graph
from langgraph.graph import StateGraph, START, END

def main():
    # Configurar el grafo de estado
    builder = StateGraph(State)

    # Definir y añadir los nodos
    builder.add_node("primary_assistant", primary_assistant)
    builder.add_node("book_hotel", hotel_booking_assistant)
    builder.add_node("book_excursion", excursion_assistant)

    # Añadir edges y lógica de enrutamiento

    # Compilar el grafo y ejecutarlo
    part_4_graph = builder.compile()
    config = RunnableConfig()
    part_4_graph.invoke({"messages": ("user", "Necesito un hotel en Santiago.")}, config)

class ChatInputType(BaseModel):
    input: List[Union[HumanMessage, AIMessage, SystemMessage]]

def start() -> None:
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8000"
        ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_routes(app, graph, path="/chat", playground_type="chat")
    print("starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()