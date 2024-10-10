import __init__
from assistant import CompleteOrEscalate
from langchain_core.prompts import ChatPromptTemplate
from tools.hotel_tools import get_availability_for_hotels, get_town_id_for_hotels, get_availability_by_hotel_id, create_hotel_booking, update_hotel_booking, cancel_hotel_booking
from datetime import datetime
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

book_hotel_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for handling hotel bookings. "
            "The primary assistant delegates work to you whenever the user needs help booking a hotel. "
            "Search for available hotels based on the user's preferences and confirm the booking details with the customer. "
            "Return the user a maximum of 3 hotel options (unless the number of results is less), with the following format: "
            "Hotel Name: Diego de Almagro Providencia"
            "Stars: ★★★"
            "Address: San Pío X 2530, Santiago, Providencia, Región Metropolitana, Chile"
            "Price from: $129.21 USD (or CLP, as the case may be)"
            "If the user wants to know more information about a specific hotel, or are interested in a hotel option, "
            "you have to bring all the availability information avilable for the hotel id. Use the 'get_hotel_info' tool for this purpose."
            "When you have the hotel availability, you have to show the rooms available with the following format: "
            "Room type: Standard"
            "Price: $129.21 USD (or CLP, as the case may be)"
            "When searching, be persistent. Expand your query bounds if the first search returns no results. "
            "If you need more information or the customer changes their mind, escalate the task back to the main assistant."
            " Remember that a booking isn't completed until after the relevant tool has successfully been used."
            "\nCurrent time: {time}."
            '\n\nIf the user needs help, and none of your tools are appropriate for it, then "CompleteOrEscalate" the dialog to the host assistant.'
            " Do not waste the user's time. Do not make up invalid tools or functions."
            "\n\nSome examples for which you should CompleteOrEscalate:\n"
            " - 'what's the weather like this time of year?'\n"
            " - 'nevermind i think I'll book separately'\n"
            " - 'i need to figure out transportation while i'm there'\n"
            " - 'Oh wait i haven't booked my flight yet i'll do that first'\n"
            " - 'Hotel booking confirmed'",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

book_hotel_safe_tools = [get_availability_for_hotels, get_town_id_for_hotels, get_availability_by_hotel_id]
book_hotel_sensitive_tools = [create_hotel_booking, update_hotel_booking, cancel_hotel_booking]
book_hotel_tools = book_hotel_safe_tools + book_hotel_sensitive_tools
book_hotel_runnable = book_hotel_prompt | llm.bind_tools(
    book_hotel_tools + [CompleteOrEscalate]
)