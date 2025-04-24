import requests
import json
import pycountry

def get_address_components(address):
    # Your API Key
    api_key = 'AIzaSyCfJuyMJj0DO3v1hXbVukQh5C2VIjvCsQw'
    
    # Google Maps Geocoding API endpoint
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    
    # Make a request to the API
    response = requests.get(url)
    
    # Parse the JSON response
    data = response.json()

    result = {
        "status" : "FAILED",
        "postalAddress" : {}
    }
    
    if data['status'] == 'OK':
        result['status'] = "ACCURATE"

        # Extract address components
        address_components = data['results'][0]['address_components']
        
        postal_address = {
            'department': None,
            'subDepartment': None,
            'streetName': None,
            'buildingNumber': None,
            'buildingName': None,
            'floor': None,
            'postBox': None,
            'room': None,
            'postCode': None,
            'townName': None,
            'townLocationName': None,
            'districtName': None,
            'countrySubDivision': None,
            'country': None,
            'countryName': None
        }
        
        # Loop through the components to find the relevant ones
        for component in address_components:
            long_name = component['long_name']
            types = component['types']
            
            if 'route' in types:  # Street name
                postal_address['streetName'] = long_name
            elif 'street_number' in types:  # Building number
                postal_address['buildingNumber'] = long_name
            elif 'premise' in types:  # Building name
                postal_address['buildingName'] = long_name
            elif 'subpremise' in types:  # Sub-building (e.g., floor or room)
                postal_address['room'] = long_name
            elif 'postal_code' in types:  # Postal code
                postal_address['postCode'] = long_name
            elif 'locality' in types:  # Town name (or city)
                postal_address['townName'] = long_name
            elif 'administrative_area_level_1' in types:  # State
                postal_address['countrySubDivision'] = long_name
            elif 'administrative_area_level_2' in types:  # District/Region
                postal_address['districtName'] = long_name
            elif 'country' in types:  # Country
                postal_address['country'] = long_name
                postal_address['countryName'] = long_name
            elif 'neighborhood' in types:  # Neighborhood name (if present)
                postal_address['townLocationName'] = long_name

            for component in address_components:
                if 'country' in component['types']:
                    # ISO country code is in 'short_name' of 'country' component
                    postal_address['countryIsoCode'] = component['short_name']
        
        result["postalAddress"] = postal_address
    elif data['status'] == 'ZERO_RESULTS':
        result['status'] = 'FAILED'
    else:
        result['status'] = 'PARTIALLY ACCURATE'
    
    return result

# Test with an example address
address = '3622 Lyckan PKWY 3003 Durham NC 27707 USA US US'
result = get_address_components(address)

print(json.dumps(result, indent = 1))
