import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

# producer
# GET_verb = "verb=GET,"
producer_verb = "GET"
producer_verb_key=f"verb={producer_verb},"
# vehicles = "/identity/api/v2/vehicle/vehicles"
producer_uri = "/2.0/users/{username}"
# vehicles_uri = f"uri={vehicles}"
producer_uri_key = f"uri={producer_uri}"
# vehicles_request = f"Request to {vehicles}"
producer_request = f"Request to {producer_uri}"
# vehicles_response = "uuid"
producer_response = "username"
producer_parameter = "username paramter"

# consumer
consumer_verb = "GET"
consumer_verb_key=f"verb={producer_verb},"
#location = "/identity/api/v2/vehicle/vehicles/{uuid}/location"
consumer_uri = "/2.0/repositories/{username}"
#location_uri = f"uri={location}"
consumer_uri_key = f"uri={consumer_uri}"
#location_request = f"Request to {location}"
consumer_request = f"Request to {consumer_uri}"
#location_response = "response to " + location
consumer_response = "response to " + consumer_uri

# References: https://www.ibisc.univ-evry.fr/~fpommereau/SNAKES/index.html

def factory (cons, prod, init_producer_request=[], init_producer_parameter=[]) :
    n = PetriNet("N")

    # /2.0/users/{username}
    # request to the producer
    n.add_place(Place(producer_request, init_producer_request))

    # parameter to the producer
    n.add_place(Place(producer_parameter, init_producer_parameter))

    t0 = Transition(producer_uri)
    n.add_transition(t0)

    # request to the consumer
    n.add_place(Place(consumer_request, []))
    # username obtained from consumer
    n.add_place(Place(producer_response, []))
    # conections
    n.add_input(producer_request, producer_uri, Value(producer_verb_key+producer_uri))
    n.add_input(producer_parameter, producer_uri, cons)

    n.add_output(consumer_request, producer_uri, Value(producer_verb_key+consumer_uri))
    n.add_output(producer_response, producer_uri, cons)

    # /2.0/repositories/{username}
    n.add_place(Place(consumer_response, []))
    t1 = Transition(consumer_uri)
    n.add_transition(t1)
    n.add_input(consumer_request, consumer_uri, Value(consumer_verb_key+consumer_uri))
    n.add_input(producer_response, consumer_uri, cons)
    n.add_output(consumer_response, consumer_uri, prod)

    return n, [t0, t1]

# source venv/bin/activate
# python3 snakes_crAPI-01.py
def main():
    # create the petri net
    net, transitions = factory(Variable("username"), Value("repository"), producer_verb_key+producer_uri, "Username01")
    net.draw("value-0.png")
    import ipdb; ipdb.set_trace()

    # given the request "/2.0/users/{username}"
    #transitions[0].fire(Substitution(username="ec62eb7c-1fb3-4a34-b188-772520778f8b"))
    transitions[0].fire(Substitution(username="Username01"))
    net.draw("value-1.png")

    #
    try:
        transitions[1].fire(Substitution(username="ec62eb7c-1fb3-4a34-b188-772520778f8b"))
    except:
        print("IDOR Attack Detected")
    net.draw("value-2.png")



# # source venv/bin/activate
# # python3 snakes_crAPI-01.py
# def main():
#     # create the petri net
#     n = PetriNet("N")
#     # request 1
#     n.add_place(Place(producer_request, producer_verb_key+producer_uri))
#     t0 = Transition(producer_uri)
#     n.add_transition(t0)
#     # response 1
#     n.add_place(Place(producer_response, []))
#     # connect
#     n.add_input(producer_request, producer_uri, Value(producer_verb_key+producer_uri))
#     n.add_output(producer_response, producer_uri, Variable("username"))

if __name__ == "__main__":
    main()
