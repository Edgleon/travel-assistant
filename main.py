from assistants.hotel_booking import hotel_booking_assistant
from assistants.excursion_booking import excursion_assistant
from tools.hotel_tools import get_availability_for_hotels
from tools.excursion_tools import get_availability_for_excursions
from langchain_core.runnables import RunnableConfig
from state import State
from assistants.primary import primary_assistant


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

if __name__ == "__main__":
    main()