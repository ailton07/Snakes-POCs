from prance import ResolvingParser
import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *


class OpenAPI2PetriNet:

    parser = ''

    def get_parser(self):
        return self.parser

    def __init__ (self, path) :
        self.parser = ResolvingParser(path)

    def create_petri_net(self):
        petri_net = PetriNet('Juice Shop')
        
        spec = self.parser.specification
        paths = spec.get('paths')

        for pathKey, pathValue in spec.get('paths').items():
            #uri_login =  "/rest/user/login"
            uri = pathKey
            # transition 1
            # creating basic structure
            transition = self.create_transition_and_basic_places(petri_net, uri)
        
            # cheking the OperationObjects
            for operationObjectKey, operationObjectValue in pathValue.items():

                requestBody = operationObjectValue.get('requestBody')
                self.handle_request_body(petri_net, transition, requestBody)

                parameters = operationObjectValue.get('parameters')
                self.handle_parameters(petri_net, transition, parameters)

                responses = operationObjectValue.get('responses')
                self.handle_responses(petri_net, uri, transition, responses)
    
        return petri_net

    def create_transition_and_basic_places(self, petri_net, uri_login):
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

    def handle_responses(self, petri_net, uri, transition, responses):
        if (responses):
            for responseKey, responseValue in responses.items():
                content = responseValue.get('content')
                for contentKey, contentValue in content.items():
                    content_type = contentKey
                    schema = contentValue.get('schema')
                    place = Place(f'Response-{uri}', [])
                    petri_net.add_place(place)
                    petri_net.add_output(place.name, transition.name, Expression("request.get_response()"))

    def handle_parameters(self, petri_net, transition, parameters):
        if (parameters):
            for parameter in parameters:
                self.create_place_and_connect_as_input(petri_net, transition, parameter.get('name'))

    def handle_request_body(self, petri_net, transition, requestBody):
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
                            self.create_place_and_connect_as_input(petri_net, transition, property_name)

    def create_place_and_connect_as_input(self, petri_net, transition, property_name):
        place = Place(property_name, [])
        petri_net.add_place(place)
        petri_net.add_input(place.name, transition.name, Variable(property_name))

    def create_place_and_connect_as_output(self, petri_net, transition, property_name):
        place = Place(property_name, [])
        petri_net.add_place(place)
        petri_net.add_output(place.name, transition.name, Variable(property_name))