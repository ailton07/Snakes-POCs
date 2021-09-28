import json
import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

# JSON file
file = open ('LoggerPlusPlus.json', "r")
data = json.loads(file.read())

network = PetriNet("N")
places_dictionary = {}
transitions_dictionary = {}

for request_response_pair in data:
    request = request_response_pair['Request']
    request_line = request['Headers'][0]
    http_verb = request_line.split()[0]
    uri = request_line.split()[1]

    response = request_response_pair['Response']
    print(request_line)

    # create places

    place = Place(request_line, request_line)
    if (places_dictionary.get(request_line)):
        continue
    places_dictionary[request_line] = place
    network.add_place(place)

    # create transitions
    transition = Transition(uri)
    network.add_transition(transition)
    transitions_dictionary[uri] = transition

    # connect
    network.add_input(request_line, uri, Value(request_line))

    # analyze parameters in body
    if http_verb == "POST":
        try:
            body_request = json.loads(request['Body'])
            for key in body_request:
                # create place
                key_place_name = 'input-' + uri + '-' + key
                key_place = Place(key_place_name, body_request[key])
                if (places_dictionary.get(key_place_name)):
                    continue
                places_dictionary[key_place_name] = key_place
                network.add_place(key_place)
                # connect
                network.add_input(key_place_name, uri, Variable(key))
        except:
            pass

    # create output places
    try:
        body_response = json.loads(response['Body'])
        for key in body_response:
             # create place
            key_place_name = 'output-' + uri + '-' + key
            key_place = Place(key_place_name, [])
            if (places_dictionary.get(key_place_name)):
                continue
            places_dictionary[key_place_name] = key_place
            network.add_place(key_place)
            # connect
            network.add_output(key_place_name, uri, Variable(key))
    except:
        pass

network.draw("value-0.png")
import ipdb;
ipdb.set_trace()
transitions_dictionary.get('/identity/api/auth/login').fire(Substitution(type="1", token="2", message="3", email='runkixt@gmail.com', password='@Root123'))

network.draw("value-0.png")
    

#import ipdb;
#ipdb.set_trace()