import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *
# producer
GET_verb = "verb=GET,"
vehicles = "/identity/api/v2/vehicle/vehicles"
vehicles_uri = f"uri={vehicles}"
vehicles_request = f"Request to {vehicles}"
vehicles_response = "uuid"
# consumer
location = "/identity/api/v2/vehicle/vehicles/{uuid}/location"
location_uri = f"uri={location}"
location_request = f"Request to {location}"
location_response = "response to " + location

# References: https://www.ibisc.univ-evry.fr/~fpommereau/SNAKES/index.html

def factory (cons, prod, init=[]) :
    n = PetriNet("N")

    # /identity/api/v2/vehicle/vehicles
    n.add_place(Place(vehicles_request, init))
    t0 = Transition(vehicles)
    n.add_transition(t0)
    # request to location
    n.add_place(Place(location_request, []))
    # uuid obtainet from vehicles
    n.add_place(Place(vehicles_response, []))
    n.add_input(vehicles_request, vehicles, Value(GET_verb+vehicles_uri))
    n.add_output(location_request, vehicles, Value(GET_verb+location_uri))
    n.add_output(vehicles_response, vehicles, cons)

    # /identity/api/v2/vehicle/vehicles/{carId}/location
    n.add_place(Place(location_response, []))
    t1 = Transition(location)
    n.add_transition(t1)
    n.add_input(location_request, location, Value(GET_verb+location_uri))
    n.add_input(vehicles_response, location, cons)
    n.add_output(location_response, location, prod)

    return n, [t0, t1]

# source venv/bin/activate
# python3 snakes_crAPI-01.py
def main():
    # create the petri net
    n = PetriNet("N")
    # request 1
    n.add_place(Place(vehicles_request, GET_verb+vehicles_uri))
    t0 = Transition(vehicles)
    n.add_transition(t0)
    # response 1
    n.add_place(Place(vehicles_response, []))
    # connect
    n.add_input(vehicles_request, vehicles, Value(GET_verb+vehicles_uri))
    n.add_output(vehicles_response, vehicles, Variable("uuid"))

    # draw
    n.draw("value-0.png")
    import ipdb; ipdb.set_trace()


    linked_variable="uuid"
    net, transitions = factory(Variable("uuid"), Value("vehicleLocation"), GET_verb+vehicles_uri)
    net.draw("value-0.png")
    import ipdb; ipdb.set_trace()

    # given the request "/identity/api/v2/vehicle/vehicles"
    transitions[0].fire(Substitution(uuid="ec62eb7c-1fb3-4a34-b188-772520778f8b"))
    net.draw("value-1.png")

    #
    try:
        transitions[1].fire(Substitution(uuid="ec62eb7c-1fb3-4a34-b188-772520778f8b"))
    except:
        print("IDOR Attack Detected")
    net.draw("value-2.png")

# def factory (cons, prod, init=[]) :
#     n = PetriNet("N")
#
#     # /identity/api/v2/vehicle/vehicles
#     n.add_place(Place(vehicles_request, init))
#     t0 = Transition(vehicles)
#     n.add_transition(t0)
#     # request to location
#     n.add_place(Place(location_request, []))
#     # uuid obtainet from vehicles
#     n.add_place(Place(vehicles_response, []))
#     n.add_input(vehicles_request, vehicles, Value(GET_verb+vehicles_uri))
#     n.add_output(location_request, vehicles, Value(GET_verb+location_uri))
#     n.add_output(vehicles_response, vehicles, cons)
#
#     # /identity/api/v2/vehicle/vehicles/{carId}/location
#     n.add_place(Place(location_response, []))
#     t1 = Transition(location)
#     n.add_transition(t1)
#     n.add_input(location_request, location, Value(GET_verb+location_uri))
#     n.add_input(vehicles_response, location, cons)
#     n.add_output(location_response, location, prod)
#
#     return n, [t0, t1]

# def main():
#     linked_variable="uuid"
#     net, transitions = factory(Variable("uuid"), Value("vehicleLocation"), GET_verb+vehicles_uri)
#     net.draw("value-0.png")
#     import ipdb; ipdb.set_trace()
#
#     # given the request "/identity/api/v2/vehicle/vehicles"
#     transitions[0].fire(Substitution(uuid="ec62eb7c-1fb3-4a34-b188-772520778f8b"))
#     net.draw("value-1.png")
#
#     #
#     try:
#         transitions[1].fire(Substitution(uuid="ec62eb7c-1fb3-4a34-b188-772520778f8b"))
#     except:
#         print("IDOR Attack Detected")
#     net.draw("value-2.png")

if __name__ == "__main__":
    main()
