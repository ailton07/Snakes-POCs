import json
from ColouredToken import ColouredToken, RequestResponseToken
#from openapi_core import create_spec
from prance import ResolvingParser
from numpy import place
from utils.log_utils import LogUtils
from utils.string_utils import StringUtils
import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

# This version create the places using the spec

# Instruções no livro Web Scraping com Pyhton
# source venv/bin/activate

# loading log
logs_file = open('logs/combined_login.json')
logs_json = json.load(logs_file)
logs_file.close()

# loading OpenAPI
# Convert YAML to JSON https://www.convertjson.com/yaml-to-json.htm
# with open('examples/JuiceShop.json', 'r') as spec_file:
#    spec_dict = json.load(spec_file)
# spec = create_spec(spec_dict)
parser = ResolvingParser('examples/JuiceShop.yaml')


def create_transition_and_basic_places(petri_net, uri_login):
    place_req = Place("Req-"+uri_login, [])

    # creating transition
    transition =  Transition(uri_login)

    # creating outputs to the transition
    place_status = Place("Status-"+uri_login, [])

    # conecting places to the transtion
    petri_net.add_place(place_req)
    petri_net.add_place(place_status)
    petri_net.add_transition(transition)
    petri_net.add_input(place_req.name, transition.name, Variable("request"))
    petri_net.add_output(place_status.name, transition.name, Expression("request.get_status()"))

    return transition

def create_petri_net():

    petri_net = PetriNet('Juice Shop')
    
    #paths = spec.get('paths')
    spec = parser.specification
    paths = spec.get('paths')

    for pathKey, pathValue in spec.get('paths').items():
        #uri_login =  "/rest/user/login"
        uri = pathKey
        # transition 1
        # creating basic structure
        transition = create_transition_and_basic_places(petri_net, uri)
    
        # cheking the OperationObjects
        for operationObjectKey, operationObjectValue in pathValue.items():

            requestBody = operationObjectValue.get('requestBody')
            handle_request_body(petri_net, transition, requestBody)

            parameters = operationObjectValue.get('parameters')
            handle_parameters(petri_net, transition, parameters)

            responses = operationObjectValue.get('responses')
            handle_responses(petri_net, uri, transition, responses)
                    

    # # creating inputs to the transition 1
    # place_input_email = Place("email", [])
    # place_input_password = Place("password", [])

    # # creating outputs to the transition 1
    # place_output_authentication = Place("authentication", [])
    # place_input_output_bid = Place("bid", [])

    # # conecting places to the transtion 1
    # petri_net.add_place(place_input_email)
    # petri_net.add_place(place_input_password)
    # petri_net.add_place(place_output_authentication)
    # petri_net.add_place(place_input_output_bid)

    # petri_net.add_input(place_input_email.name, transition_1.name, Variable("email"))
    # petri_net.add_input(place_input_password.name, transition_1.name, Variable("password"))
    # petri_net.add_output(place_output_authentication.name, transition_1.name, Variable("authentication"))
    # petri_net.add_output(place_input_output_bid.name, transition_1.name, Expression("authentication.get_element_from_dict('bid')"))

    # # transition 2
    # uri_login =  "/rest/basket/{basketId}"
    # transition_2 = create_transition_and_basic_places(petri_net, uri_login)
    # petri_net.add_input(place_input_output_bid.name, transition_2.name, Variable("id"))

    return petri_net

def handle_responses(petri_net, uri, transition, responses):
    if (responses):
        for responseKey, responseValue in responses.items():
            content = responseValue.get('content')
            for contentKey, contentValue in content.items():
                content_type = contentKey
                schema = contentValue.get('schema')
                place = Place(f'Response-{uri}', [])
                petri_net.add_place(place)
                petri_net.add_output(place.name, transition.name, Expression("request.get_response()"))

def handle_parameters(petri_net, transition, parameters):
    if (parameters):
        for parameter in parameters:
            create_place_and_connect_as_input(petri_net, transition, parameter.get('name'))

def handle_request_body(petri_net, transition, requestBody):
    if (requestBody):
        content = requestBody.get('content')
        for contentKey, contentValue in content.items():
            if (contentValue.get('schema')):
                schema = contentValue.get('schema')
                # possible values of schema type https://yaml.org/spec/1.2-old/spec.html#id2803231
                type = schema.get('type')
                if (type == 'object'):
                    properties = schema.get('properties')
                    for property_key, property_value in properties.items():
                        property_name = property_key
                                #property_type = property_value.get('type')
                        create_place_and_connect_as_input(petri_net, transition, property_name)

def create_place_and_connect_as_input(petri_net, transition, property_name):
    place = Place(property_name, [])
    petri_net.add_place(place)
    petri_net.add_input(place.name, transition.name, Variable(property_name))

def create_place_and_connect_as_output(petri_net, transition, property_name):
    place = Place(property_name, [])
    petri_net.add_place(place)
    petri_net.add_output(place.name, transition.name, Variable(property_name))


def get_place_by_name(petri_net, name):
    return [x for x in petri_net.place() if x.name == name][0]


def fill_input_places(petri_net, log_json):
    if (log_json.get('uri') in [x.name for x in petri_net.transition()]):
        place_req_name='Req-'+log_json.get('uri')
        #place = [x for x in petri_net.place() if x.name == place_req_name][0]
        place = get_place_by_name(petri_net, place_req_name)
        #place.tokens.add(json.dumps(LogUtils.create_request_line_from_log(log_json)))
        place.tokens.add(ColouredToken(LogUtils.create_request_line_from_log(log_json)))

        # given a transistion, check if we have some input to set
        request_body_parameter_names = [*log_json.get('requestBody').keys()] # convert dict to array
        transition = [x for x in petri_net.transition() if x.name == log_json.get('uri')][0]
        places = transition.input()
        for parameter_name in request_body_parameter_names:
            for place in places:
                if place[0].name == parameter_name:
                    place[0].add(ColouredToken(LogUtils.create_data_from_request_body_in_log(log_json, parameter_name)))
                    continue
    else:
        for transition in petri_net.transition():
            if (StringUtils.compare_uri_with_model(transition.name, log_json.get('uri') )):
                place_req_name='Req-'+transition.name
                place = get_place_by_name(petri_net, place_req_name)
                place.tokens.add(ColouredToken(LogUtils.create_request_line_from_log(log_json)))
    



def main():
    petri_net = create_petri_net()
    transitions = petri_net.transition()
    petri_net.draw("value-0.png")

    log_line = logs_json[1]
    fill_input_places(petri_net, log_line)
    
    import ipdb; ipdb.set_trace()

    request_line = RequestResponseToken(*LogUtils.create_request_request_response_from_log(log_line))
    email=ColouredToken(LogUtils.create_data_from_request_body_in_log(log_line, 'email'))
    password=ColouredToken(LogUtils.create_data_from_request_body_in_log(log_line, 'password'))
    authentication = ColouredToken(LogUtils.create_response_data_from_log(log_line, 'authentication'))

    import ipdb; ipdb.set_trace()
    #transition_1.fire(Substitution(request=request_line, email=email, password=password, status=response_status, authentication=authentication))
    transitions[0].fire(Substitution(request=request_line, email=email, password=password, authentication=authentication))
    petri_net.draw("value-0.png")
    
    
    petri_net.draw("value-0.png")


if __name__ == "__main__":
    main()
