from fastapi import FastAPI, WebSocket
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langgraph.graph import StateGraph
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages import ToolMessage
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from graph import runnable_instance as graph, part_4_graph
from state import State
from assistants.primary import assistant_runnable
from utilities import _print_event
import uuid
import uvicorn
from typing import List, Union
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

class ChatInputType(BaseModel):
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)
thread_id = str(uuid.uuid4())
builder = StateGraph(State)
_printed = set()

#part_4_graph = builder.compile()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# @app.websocket("/chat")
# # async def redirect_root_to_docs():
# #     return RedirectResponse("/docs")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     config = {"configurable": {"thread_id": thread_id}}
#     while True:
#         user_message = await websocket.receive_text()
#         events = graph.stream(
#             {"messages": ("user", user_message)}, config, stream_mode="values"
#         )
#         for event in events:
#             _print_event(event, _printed)
#         snapshot = graph.get_state(config)
#         user_input = input(
#             "Do you approve of the above actions? Type 'y' to continue;"
#             " otherwise, explain your requested changed.\n\n"
#         )
#         if user_input.strip() == "y":
#             # Just continue
#             result = graph.invoke(
#                 None,
#                 config,
#             )
#         else:
#             result = graph.invoke(
#                 {
#                     "messages": [
#                         ToolMessage(part_1_toolsext(result["messages"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Edit this to add the chain you want to add
# unnable = part_4_graph.with_types(input_type=ChatInputType, output_type=dict)
from langserve.serialization import serialize

add_routes(
    app,
    graph.with_types(input_type=ChatInputType, output_type=dict),
    path="/chat",
    playground_type="default",
    serializer=serialize,
)
print("starting server...")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



