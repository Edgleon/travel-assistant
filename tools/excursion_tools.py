from typing import Optional
import requests
import os
from tools.tool import tool


@tool
def get_availability_for_transfer_and_excursions(
    townId: Optional[int] = None,
    tipos: Optional[int] = None,
    fecha: Optional[str] = None,
    adults: Optional[int] = 1,
    children: Optional[int] = 0,
    currency: Optional[int] = 1,
    ) -> list[dict]:
    """
    Get availability of transport or excursions in a given town.

    Args:
    townId: The town ID.
    tipos: The type of service. 1 is for transfer, and 2 is for excursions.
    fecha (string): The date (format YYYY-MM-DD).
    adults: The number of adults. Default is 1.
    children: The number of children. Default is 0.
    currency: The currency. 1 is for CLP, and 2 is for USD. Default is 1.

    Returns:
    A list of dictionaries containing the availability of
    transport or excursions in the given town.

    Example:
    get_availability_for_transport_and_excursions(townId='1234', tipos='1', fecha='2024-12-01', adults=2, children=1, currency=1)
    """

    url = f'{os.getenv("CTS_API_V2")}/availability/?townId={townId}&tipos={tipos}&fecha={fecha}&adults={adults}&children={children}&currency={currency}'
    ctsToken = os.getenv("CTS_TOKEN")
    headers = {'Authorization': f'token {ctsToken}'}
    response = requests.get(url, headers=headers)
    #TODO
    if tipos == 1:
        result = generate_transfer_availability_response(response.json())
    if tipos == 2:
        result = generate_excursion_availability_response(response.json())
    return result

@tool
def get_town_id_for_transport_and_excursions(townName: str) -> list[dict]:
    """
    Get the town ID.

    Args:
    townName: The town or city name.

    Returns:
    The Town ID.

    Example:
    get_town_id_for_transport_and_excursions('santiago')
    """
    url = f'{os.getenv("CTS_API_V2")}/city/'
    ctsToken = os.getenv("CTS_TOKEN")
    headers = {'Authorization': f'token {ctsToken}'}
    response = requests.get(url, headers=headers)

    for town in response.json():
        if town['name'].lower() == townName.lower():
            return town['id']
        
    return None
#TODO
@tool
def create_transport_or_excursion_booking() -> list[dict]:
    """
    Create a transport or excursion booking.

    Returns:
    The booking ID.

    Example:
    create_transport_or_excursion_booking()
    """
    url = f'{os.getenv("CTS_API_V2")}/booking/'
    ctsToken = os.getenv("CTS_TOKEN")
    headers = {'Authorization': f'token {ctsToken}'}
    response = requests.post(url, headers=headers)
    return response.json()

#TODO
@tool
def update_transport_or_excursion_booking() -> list[dict]:
    """
    Update a transport or excursion booking.

    Returns:
    The booking ID.

    Example:
    update_transport_or_excursion_booking()
    """
    url = f'{os.getenv("CTS_API_V2")}/booking/'
    ctsToken = os.getenv("CTS_TOKEN")
    headers = {'Authorization': f'token {ctsToken}'}
    response = requests.put(url, headers=headers)
    return response.json()

#TODO
@tool
def cancel_transport_or_excursion_booking(bookingId: str) -> list[dict]:
    """
    Cancel a transport or excursion booking.

    Args:
    bookingId: The booking ID.
    
    Returns:
    The booking ID.
    
    Example:
    cancel_transport_or_excursion_booking('1234')
    """
    url = f'{os.getenv("CTS_API_V2")}/booking/{bookingId}/'
    ctsToken = os.getenv("CTS_TOKEN")
    headers = {'Authorization': f'token {ctsToken}'}
    response = requests.delete(url, headers=headers)
    return response.json()