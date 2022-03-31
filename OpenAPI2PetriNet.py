import snakes.plugins
from ColouredToken import ColouredToken, RequestResponseToken
from prance import ResolvingParser
snakes.plugins.load("gv", "snakes.nets", "nets")
from utils.log_utils import LogUtils
from utils.string_utils import StringUtils
from nets import *


class OpenAPI2PetriNet:

    parser = ''

    def get_parser(self):
        return self.parser

    def __init__ (self, path) :
        self.parser = ResolvingParser(path)

    def create_petri_net(self, name):
        petri_net = PetriNet(name)
        
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

    def get_place_by_name(self, petri_net, name):
        response = [x for x in petri_net.place() if x.name == name]
        if (response and len(response) > 0):
            return response[0]
        else:
            # se o place nao foi encontrado pelo metodo anterior, e possivel que o path tenha um
            # parametro
            response = [x for x in petri_net.place() if StringUtils.compare_uri_with_model(x.name, name)]
            if (response and len(response) > 0):
                return response[0]
        return None

    def get_transition_by_name(self, petri_net, name):
        response = [x for x in petri_net.transition() if x.name == name]
        if (response and len(response) > 0):
            return response[0]
        else:
            # se o place nao foi encontrado pelo metodo anterior, e possivel que o path tenha um
            # parametro
            response = [x for x in petri_net.transition() if StringUtils.compare_uri_with_model(x.name, name)]
            if (response and len(response) > 0):
                return response[0]
        return None


        

    # def fill_input_places(self, petri_net, log_json):
    #     if (log_json.get('uri') in [x.name for x in petri_net.transition()]):
    #         # setting tokens related to RequestLine
    #         place_req_name='Req-'+log_json.get('uri')
    #         place = self.get_place_by_name(petri_net, place_req_name)
    #         place.tokens.add(ColouredToken(LogUtils.create_request_line_from_log(log_json)))

    #         # given a transistion, check if we have some input to set
    #         # setting tokens related to requestBody
    #         request_body_parameter_names = [*log_json.get('requestBody').keys()] # convert dict to array
    #         transition = [x for x in petri_net.transition() if x.name == log_json.get('uri')][0]
    #         places = transition.input()
    #         for parameter_name in request_body_parameter_names:
    #             for place in places:
    #                 if place[0].name == parameter_name:
    #                     place[0].add(ColouredToken(LogUtils.create_data_from_request_body_in_log(log_json, parameter_name)))
    #                     continue
    #         # setting tokens related to parameters
    #     else:
    #         # setting tokens
    #         for transition in petri_net.transition():
    #             if (StringUtils.compare_uri_with_model(transition.name, log_json.get('uri') )):
    #                 place_req_name='Req-'+transition.name
    #                 place = self.get_place_by_name(petri_net, place_req_name)
    #                 place.tokens.add(ColouredToken(LogUtils.create_request_line_from_log(log_json)))

    def place_is_output(self, petri_net, place):
        #import ipdb; ipdb.set_trace()
        transitions = petri_net.transition()
        for transition in transitions:
            for output in transition.output():
                if output[0].name == place.name:
                    return True

        return False



    def fill_input_places(self, petri_net, log_json):
        for transition in petri_net.transition():
            if (StringUtils.compare_uri_with_model(transition.name, log_json.get('uri') )):
                # setting tokens related to RequestLine
                place_req_name='Req-'+log_json.get('uri')
                place = self.get_place_by_name(petri_net, place_req_name)
                if place:
                    place.tokens.add(ColouredToken(LogUtils.create_request_line_from_log(log_json)))

                    # given a transistion, check if we have some input to set
                    # setting tokens related to requestBody
                    request_body_parameter_names = [*log_json.get('requestBody').keys()] # convert dict to array
                    transition = self.get_transition_by_name(petri_net, log_json.get('uri'))
                    places = transition.input()
                    for parameter_name in request_body_parameter_names:
                        for place in places:
                            # se o place for output de alguma transição, nao devemos colocar tokens
                            if self.place_is_output(petri_net, place[0]):
                                continue
                            if place[0].name == parameter_name:
                                place[0].add(ColouredToken(LogUtils.create_data_from_request_body_in_log(log_json, parameter_name)))
                                break
                    # setting tokens related to parameters
        