from langchain_core.tools import tool
import os
import requests
from typing import Optional, List, Dict

@tool
def get_availability_for_hotels(
    townId: Optional[str] = None,
    checkin_date: Optional[str] = None,
    checkout_date: Optional[str] = None,
    adults: Optional[int] = 1,
    children: Optional[int] = 0,
    infants: Optional[int] = 0,
    ages: Optional[List[int]] = [],
    currency: Optional[int] = 1,
) -> List[Dict]:
    """
    Get availability of hotels in a given town.

    Args:
    townId: The town ID.
    checkin_date (string): The check-in date.
    checkout_date (string): The check-out date.
    adults: The number of adults. Default is 1.
    children: The number of children. Default is 0.
    infants: The number of infants. Default is 0.
    ages: The ages of the children. Default is [].
    currency: The currency. Default is 1.

    Returns:
    A list of dictionaries containing the availability of
    hotels in the given town.

    Example:
    get_availability(townId='1234', checkin_date='2022-12-01', checkout_date='2022-12-05', adults=2, children=1)    
    """
    url = 'https://apibooking.ctsturismo.com/api/hotel/'

    ctsToken = os.getenv("CTS_TOKEN")
    headers = {'Authorization': f'token {ctsToken}'}
    json = {'townId': townId, 'checkin': checkin_date, 'checkout': checkout_date, 'rooms': [{'adults': adults, 'children': children, 'infants': infants, 'ages': ages}], 'currency': currency}
    response = requests.post(url, json=json, headers=headers)
    result = generate_hotels_availability_response(response.json())
    return result

@tool
def get_hotel_info(
    hotelId: str,
    townId: Optional[str] = None,
    checkin_date: Optional[str] = None,
    checkout_date: Optional[str] = None,
    adults: Optional[int] = 1,
    children: Optional[int] = 0,
    infants: Optional[int] = 0,
    ages: Optional[list[int]] = [],
    currency: Optional[int] = 1,
) -> list[dict]:
    """
    Get availability of hotels in a given town.

    Args:
    hotelId: The hotel ID.
    townId: The town ID.
    checkin_date (string): The check-in date.
    checkout_date (string): The check-out date.
    adults: The number of adults. Default is 1.
    children: The number of children. Default is 0.
    infants: The number of infants. Default is 0.
    ages: The ages of the children. Default is [].
    currency: The currency. Default is 1.

    Use this function when the user wants to know more information of the hotel
    or has already selected a hotel.

    Returns:
    A list of dictionaries containing the availability of
    one hotel in the given hotel id.

    Example:
    get_availability(hotelId = '196', townId='1234', checkin_date='2022-12-01', checkout_date='2022-12-05', adults=2, children=1)    
    """
    url = f'{os.getenv("CTS_API_V1")}/hotel/{hotelId}/'

    ctsToken = os.getenv("CTS_TOKEN")
    headers = {'Authorization': f'token {ctsToken}'}
    json = {'townId': townId, 'checkin': checkin_date, 'checkout': checkout_date, 'rooms': [{'adults': adults, 'children': children, 'infants': infants, 'ages': ages}], 'currency': currency}
    response = requests.post(url, json=json, headers=headers)
    result = response.json()
    return result

@tool
def get_town_id_for_hotels(townName: str) -> List[Dict]:
    """
    Get the town ID.

    Args:
    townName: The town or city name.

    Returns:
    The Town ID.

    Example:
    get_city_id('santiago')
    """
    url = f'https://apibooking.ctsturismo.com/api/city/dtt/?q={townName}'
    ctsToken = os.getenv("CTS_TOKEN")
    headers = {'Authorization': f'token {ctsToken}'}
    response = requests.get(url, headers=headers)
    return response.json()[0]['dtt_id']

#TODO
@tool
def create_hotel_booking(
    name: str,
    last_name: str,
    passport_or_dni: str,
    email: str,
    phone: str,
    country: str,
    notes: str,
    currency: str,
    adults: int,
    children: int,
    infants: int,
    total_amount: int,
    total_net_amount: int,
    total_collect_amount: int,
    user: int,
    hotel_id: int,
    hotel_name: str,
    inventory_id: int,
    room_name: str,
    rate_id: int,
    travel_date: str,
    checkout_date: str,
    city: str,
    cover_image: str,
    room_amount: int
) -> dict:
    """
    Create a hotel booking.

    Returns:
    The booking response as a dictionary.
    """
    url = f'{os.getenv("CTS_API_V1")}/booking/'
    cts_token = os.getenv("CTS_TOKEN")
    headers = {'Authorization': f'token {cts_token}'}

    payload = {
        "name": name,
        "last_name": last_name,
        "passport_or_dni": passport_or_dni,
        "email": email,
        "phone": phone,
        "country": country,
        "notes": notes,
        "currency": currency,
        "adults": adults,
        "children": children,
        "infants": infants,
        "total_amount": total_amount,
        "total_net_amount": total_net_amount,
        "total_collect_amount": total_collect_amount,
        "reference_number": "",
        "user": user,
        "booking_availability": [
            {
                "hotelId": hotel_id,
                "hotelName": hotel_name,
                "inventoryIds": [
                    {
                        "inventoryId": inventory_id,
                        "roomName": room_name,
                        "rateIds": [
                            rate_id
                        ],
                        "adults": [
                            adults
                        ],
                        "amount": room_amount
                    }
                ]
            }
        ],
        "cart_items": {
            "count": 1,
            "hotels": [
                {
                    "dtt_hotel_code": hotel_id,
                    "dtt_hotel_markup": 11,
                    "glosa_visualizer": hotel_name,
                    "glosa_soptur": hotel_name,
                    "provider": "DTT",
                    "city": city,
                    "concepts": "Wifi, Breakfast, Parking, Room Service, TV, Safe, Laundry",
                    "country": city,
                    "service_type": "hotel",
                    "adults": adults,
                    "children": children,
                    "infants": infants,
                    "adult_total_amount": total_amount,
                    "children_total_amount": 0,
                    "amount": total_amount,
                    "net_amount": total_net_amount,
                    "hotel_additional_total": 0,
                    "hotel_additional_base": 0,
                    "hotel_total": total_net_amount,
                    "travel_date": travel_date,
                    "checkout": checkout_date,
                    "cover_image": cover_image,
                    "payload_detail": [
                        {
                            "date": travel_date,
                            "total": total_net_amount,
                            "total_base": int(total_net_amount * 0.89),
                            "total_with_tax": total_amount,
                            "additional_base": 0,
                            "additional_total_base": 0,
                            "additional_total_with_tax": 0,
                            "rooms": [
                                room_name
                            ]
                        }
                    ],
                    "dtt_fee_percent": 0,
                    "dtt_fee_value": 0,
                    "total_dtt": 0,
                    "rooms": [
                        {
                            "adults": adults,
                            "children": children,
                            "ages": "",
                            "discount_rate": 0,
                            "mealplan": "Breakfast Included",
                            "mealplan_id": 2,
                            "operator": "CTS Turismo",
                            "cancellation_type": "Free Cancelation",
                            "cancellation_id": 1,
                            "operator_id": 5,
                            "policies": "",
                            "currency_id": 1,
                            "roomtype": room_name,
                            "roomtype_id": 900,
                            "size": "28 mts²",
                            "bed_options": "2 Individuales",
                            "amount": room_amount,
                            "pull_inventory": False,
                            "room_for": 0,
                            "replaceMarkup": 1,
                            "rateplan_name": "CTS - CONFIDENCIAL CONV",
                            "details": [
                                {
                                    "date": travel_date,
                                    "rateplan": "CTS - CONFIDENCIAL CONV",
                                    "rateplan_id": 16465,
                                    "guest": adults,
                                    "markup": 11,
                                    "base_value": int(total_net_amount * 0.89),
                                    "total": total_net_amount,
                                    "total_with_tax": total_amount,
                                    "inventory_id": inventory_id,
                                    "rate_id": rate_id,
                                    "additional_base": 0,
                                    "additional_total_base": 0,
                                    "additional_total_with_tax": 0
                                }
                            ]
                        }
                    ],
                    "id": 3,
                    "nights": 1,
                    "hotelName": hotel_name,
                    "roomType": room_name,
                    "subTotalPrice": total_net_amount,
                    "taxPrice": total_amount - total_net_amount,
                    "totalPrice": total_amount,
                    "serviceUrl": f"/results/hotels/{hotel_id}?townId=51&checkin={travel_date}&checkout={checkout_date}&rooms=[{{%22adults%22:{adults},%22children%22:{children},%22infants%22:{infants},%22ages%22:[]}}]#rooms",
                    "item_extras": {
                        "address": "Vecinal 40, 7550226 Las Condes, Región Metropolitana, Chile",
                        "description": "Ubicado en la estación de metro El Golf, barrio que constituye el principal centro de negocios de la capital, y que se caracteriza por una variada de oferta comercial y gastronómica.",
                        "checkinHour": "14:00:00",
                        "checkoutHour": "12:00:00",
                        "hotelPhone": "2663 3152"
                    },
                    "cancellationTime": 48,
                    "additional_information": notes
                }
            ],
            "services": [],
            "packages": [],
            "createdAt": "2024-10-15T23:27:39.469Z",
            "discount": {}
        },
        "language": "es",
        "company": None
    }

    response = requests.post(url, headers=headers, json=payload)
    booking_id = response.json()['file_number']
    slug = response.json()['slug']
    booking_link = f'os.getenv("CTS_API_V1")/bookings/{slug}'
    return f'Se ha realizado la reserva con éxito. El número de reserva es {booking_id}. Puede ver los detalles de la reserva en el siguiente enlace: {booking_link}'

#TODO
@tool
def update_hotel_booking() -> List[Dict]:
    """
    Update a hotel booking.

    Returns:
    The booking ID.

    Example:
    update_hotel_booking()
    """
    # url = 'https://apibooking.ctsturismo.com/api/booking/'
    # ctsToken = os.getenv("CTS_TOKEN")
    # headers = {'Authorization': f'token {ctsToken}'}
    # response = requests.put(url, headers=headers)
    return #response.json()

#TODO
@tool
def cancel_hotel_booking(bookingId: str) -> List[Dict]:
    """
    Cancel a hotel booking.

    Args:
    bookingId: The booking ID.

    Returns:
    The booking ID.

    Example:
    cancel_hotel_booking('1234')
    """
    # url = f'https://apibooking.ctsturismo.com/api/booking/{bookingId}/'
    # ctsToken = os.getenv("CTS_TOKEN")
    # headers = {'Authorization': f'token {ctsToken}'}
    # response = requests.delete(url, headers=headers)
    return# response.json()


# Helpers

def generate_hotels_availability_response(json_response):
    result = []
    for data in json_response['data']:
        hotel = {}
        hotel['hotelId'] = data['id']
        hotel['hotelName'] = data['name']
        hotel['stars'] = data['category']['rating']
        hotel['hotelAddress'] = data['address']
        priceList = map(lambda x: x['price_value_with_tax'], data['availability'])
        hotel['priceFrom'] = min(priceList)
        result.append(hotel)
    return result