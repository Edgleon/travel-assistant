from langchain_core.tools import tool
import os
import requests
import json
import datetime
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
    hotelId: int,
    townId: Optional[str] = None,
    checkin_date: Optional[str] = None,
    checkout_date: Optional[str] = None,
    adults: Optional[int] = 1,
    children: Optional[int] = 0,
    infants: Optional[int] = 0,
    ages: Optional[list[int]] = [],
    currency: Optional[int] = 1,
    roomId: int = None,
    name: Optional[str] = "",
    lastName: Optional[str] = "",
    email: Optional[str] = "",
    phone: Optional[str] = "",
    passportOrDni: Optional[str] = "",
    country: Optional[str] = None,
    referenceNumber: Optional[str] = "",
    notes: Optional[str] = "",
) -> dict:
    """
    Create a hotel booking.

    Args:
    hotelId: The hotel ID.
    townId: The town ID.
    checkin_date (string): The check-in date, in 'YYYY-mm-dd' format.
    checkout_date (string): The check-out date, in 'YYYY-mm-dd' format.
    adults: The number of adults. Default is 1.
    children: The number of children. Default is 0.
    infants: The number of infants. Default is 0.
    ages: The ages of the children. Default is [].
    currency: The currency. 1 is for CLP, 2 for USD. Default is 1.
    roomId: The room ID.
    name: The name of the guest.
    lastName: The last name of the guest.
    email: The email of the guest.
    phone: The phone number of the guest.
    passportOrDni: The passport or DNI of the guest.
    country: The country of the guest.
    referenceNumber: The reference number.
    notes: The notes.

    Returns:
    The booking response as a string with the booking ID and
    a link to the booking detail.
    """
    try:
        hotelAvailability = get_data_for_booking(hotelId=hotelId, townId=townId, checkin_date=checkin_date, checkout_date=checkout_date, adults=adults, children=children, infants=infants, ages=ages, currency=currency)
        if not hotelAvailability:
            raise ValueError("No availabilty found for this hotel.")
        hotelData = hotelAvailability['data']
        townName = hotelData['town']['name']
        hotelName = hotelData['name']
        ammenities = hotelData['ammenities']
        concepts = ', '.join([amenity['name'] for amenity in ammenities])
        user = 1
        currency = 'CLP' if currency == 1 else 'USD'
        avail = hotelData['availability']
        availability = None
        for dispo in avail:
            for room in dispo['rooms']:
                if room['roomtype_id'] == roomId:
                    availability = dispo
        if not availability:
            raise ValueError("Room with the specified roomId not found in availability data.")
        markup = availability['markup'][0]
        bookingAvailabilityList = []
        availabilityDetails = availability['details']
        primary_image_url = next((image["url"] for image in hotelData["images"] if image["is_primary"]), None)
        rooms = availability['rooms']
        #convert checkin_date and checkout_date from 'YYY-mm-dd' to 'dd-mm-YYY'
        checkin_date_inv = datetime.strptime(checkin_date, '%Y-%m-%d').strftime('%d-%m-%Y')
        checkout_date_inv = datetime.strptime(checkout_date, '%Y-%m-%d').strftime('%d-%m-%Y')
        
        # Collecting booking information
        for room in rooms:
            inventory_ids = []
            for detail in room['details']:
                inventory_id = detail['inventory_id']
                rate_id = detail['rate_id']
                room_name = room['roomtype']
                inventory_ids.append({
                    'inventoryId': inventory_id,
                    'roomName': room_name,
                    'rateIds': [rate_id],
                    'adults': [room['adults']],
                    'amount': 1  # Assuming one room per inventory
                })

            bookingAvailabilityList.append({
                'hotelId': hotelData['id'],
                'hotelName': hotelData['name'],
                'inventoryIds': inventory_ids
            })

        # Extracting pricing and guest details
        priceBase = availability['price_base']
        priceValue = availability['price_value']
        priceValueWithTax = availability['price_value_with_tax']
        additionalBase = availability['additional_base']
        additionalTotalBase = availability['additional_total_base']
        additionalValueWithTax = availability['additional_value_with_tax']
        
        # Defining payload details
        payload_detail = [
            {
                "date": detail['date'],
                "total": detail['total'],
                "total_base": detail['total_base'],
                "total_with_tax": detail['total_with_tax'],
                "additional_base": detail['additional_base'],
                "additional_total_base": detail['additional_total_base'],
                "additional_total_with_tax": detail['additional_total_with_tax'],
                "rooms": detail['rooms']
            } for detail in availabilityDetails
        ]

        payload = {
            "name": name,
            "last_name": lastName,
            "passport_or_dni": passportOrDni,
            "email": email,
            "phone": phone,
            "country": country,
            "notes": notes,
            "currency": currency,
            "adults": adults,
            "children": children,
            "infants": infants,
            "total_amount": priceValueWithTax,
            "total_net_amount": priceValue,
            "total_collect_amount": priceValueWithTax,
            "reference_number": referenceNumber,
            "user": user,
            "booking_availability": bookingAvailabilityList,
            "cart_items": {
                "count": 1,
                "hotels": [
                    {
                        "dtt_hotel_code": hotelId,
                        "dtt_hotel_markup": markup,
                        "glosa_visualizer": hotelName,
                        "glosa_soptur": hotelName,
                        "provider": "DTT",
                        "city": townName,
                        "concepts": concepts,
                        "country": townName,
                        "service_type": "hotel",
                        "adults": adults,
                        "children": children,
                        "infants": infants,
                        "adult_total_amount": priceValueWithTax,
                        "children_total_amount": additionalValueWithTax,
                        "amount": priceValueWithTax,
                        "net_amount": priceValue,
                        "pull_inventory": "false",
                        "hotel_additional_total": additionalTotalBase,
                        "hotel_additional_base": additionalBase,
                        "hotel_total": priceBase,
                        "travel_date": checkin_date_inv,
                        "checkout": checkout_date_inv,
                        "cover_image": primary_image_url,
                        "payload_detail": payload_detail,
                        "dtt_fee_percent": 0,
                        "dtt_fee_value": 0,
                        "total_dtt": 0,
                        "rooms": rooms,
                        "id": 3,
                        "nights": 2,
                        "hotelName": hotelName,
                        "roomType": room_name,
                        "subTotalPrice": priceValue,
                        "taxPrice": priceValueWithTax - priceValue,
                        "totalPrice": priceValueWithTax,
                        "serviceUrl": f"/results/hotels/{hotelId}?townId=51&checkin={checkin_date}&checkout={checkout_date}&rooms=[{{%22adults%22:{adults},%22children%22:{children},%22infants%22:{infants},%22ages%22:[]}}]#rooms",
                        "item_extras": {
                            "address": hotelData['address'],
                            "description": hotelData['policies_description'],
                            "checkinHour": hotelData['checkin'],
                            "checkoutHour": hotelData['checkout'],
                            "hotelPhone": hotelData['phone']
                        },
                        "cancellationTime": hotelData['cancellation'],
                        "additional_information": notes
                    }
                ],
                "services": [],
                "packages": [],
                "createdAt": datetime.now().isoformat(),
                "discount": {}
            },
            "language": "es",
            "company": None
        }

        url = f'{os.getenv("CTS_API_V1")}/booking/'
        cts_token = os.getenv("CTS_TOKEN")
        headers = {'Authorization': f'token {cts_token}', 'origin': 'localhost'}

        response = requests.post(url, headers=headers, json=payload).json()

        if response:
            booking_id = response['file_number']
            slug = response['slug']
            booking_link = os.getenv("FRONT_HOST") + f'/bookings/{slug}'
            return f'Se ha realizado la reserva con éxito. El número de reserva es {booking_id}. Puede ver los detalles de la reserva en el siguiente enlace: {booking_link}'
        else:
            print("Empty response received")
            return "Error: Empty response received from the server"

    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

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
    url = f'https://apibooking.ctsturismo.com/api/booking/{bookingId}/'
    ctsToken = os.getenv("CTS_TOKEN")
    headers = {'Authorization': f'token {ctsToken}'}
    json = {'file_number': bookingId}
    response = requests.post(url, json=json, headers=headers)
    if response.status_code == 200:
        return f'La reserva con el número {bookingId} ha sido cancelada con éxito.'
    else:
        return 'No se ha podido cancelar la reserva.'

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

def get_data_for_booking(
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