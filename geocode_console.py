
def display_locations(locations=[]):
    location_count = len(locations)
    for i in range(0, location_count):
        print("{number} - {city}, {state} @{latitude},{longitude}"
            .format(
                    number=i+1,
                    city=locations[i]['adminArea5'],
                    state=locations[i]['adminArea3'],
                    latitude=locations[i]['latLng']['lat'],
                    longitude=locations[i]['latLng']['lng']
            )
        )

def get_user_location_choice(locations):
    choice_num = None

    while True:
        display_locations(locations)
        choice = input("Enter location choice: ")
        try:
            choice_num = int(choice)
            if choice_num < 1 or choice_num > len(locations):
                print("Location choice is outside the range.")
                continue
            else:
                break
        except:
            print("Location choice must be a number.")

    selected_location = locations[choice_num - 1]

    mod_selected_location = {
        'location': selected_location['adminArea5'] + ', ' + selected_location['adminArea3'],
        'latitude': selected_location['latLng']['lat'],
        'longitude': selected_location['latLng']['lng']
    }

    return mod_selected_location
    
