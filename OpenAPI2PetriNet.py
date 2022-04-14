import snakes.plugins
from ColouredToken import ColouredToken, RequestResponseToken
from prance import ResolvingParser
snakes.plugins.load("gv", "snakes.nets", "nets")
from utils.log_utils import LogUtils
from utils.string_utils import StringUtils
from nets import PetriNet, Place, Expression, Transition, Variable # added here to mute warnings
from nets import *


class OpenAPI2PetriNet:

    parser = ''
    petri_net = None

    def get_parser(self):
        return self.parser

    def __init__ (self, path) :
        self.parser = ResolvingParser(path)

    def create_petri_net(self, name, create_links=True):
        petri_net = PetriNet(name)
        
        spec = self.parser.specification
        paths = spec.get('paths')

        for path_key, path_value in spec.get('paths').items():
            uri = path_key
            # transition 1
            # creating basic structure
            transition = self.create_transition_and_basic_places(petri_net, uri)
        
            # cheking the OperationObjects
            for operation_object_key, operation_object_value in path_value.items():

                requestBody = operation_object_value.get('requestBody')
                self.handle_request_body(petri_net, transition, requestBody)

                parameters = operation_object_value.get('parameters')
                self.handle_parameters(petri_net, transition, parameters)

                responses = operation_object_value.get('responses')
                self.handle_responses(petri_net, uri, transition, responses)
        self.petri_net = petri_net

        if create_links:
            self.create_link_arcs()

        return petri_net


    def create_link_arcs(self):
        spec = self.parser.specification
        for path_key, path_value in spec.get('paths').items():
            uri = path_key
            transition = self.get_transition_by_name(uri)
            # cheking the OperationObjects
            for operation_object_key, operation_object_value in path_value.items():
                responses = operation_object_value.get('responses')
                links = self.extract_links_from_responses(responses)
                if (links):
                    for link in links:
                        for link_key, link_value in link.items():
                            operation_id = link_value.get('operationId')
                            req_place = self.get_req_place_by_operation_id(operation_id)
                            nex_transition_name = req_place.name.replace('Req-', '')
                            next_http_method = self.get_http_method_by_operation_id(operation_id)
                            self.petri_net.add_output(req_place.name, transition.name,
                                                 Expression(f"request.get_next_request('{nex_transition_name}', '{next_http_method}')"))


    def get_req_place_by_operation_id(self, operation_id):
        spec = self.parser.specification
        for path_key, path_value in spec.get('paths').items():
            uri = path_key
            for operation_object_key, operation_object_value in path_value.items():
                operationId = operation_object_value.get('operationId')
                if operationId == operation_id:
                    req_place = self.get_place_by_name(self.create_name_to_req_place(uri))
                    if req_place is None:
                        raise Exception(f'Req Place not found to uri={uri}')
                    return req_place


    def get_http_method_by_operation_id(self, operation_id):
        spec = self.parser.specification
        for path_key, path_value in spec.get('paths').items():
            uri = path_key
            for operation_object_key, operation_object_value in path_value.items():
                operationId = operation_object_value.get('operationId')
                if operationId == operation_id:
                    return operation_object_key.upper()


    def extract_links_from_responses(self, responses):
        links_set = []
        if (responses):
            for responseKey, responseValue in responses.items():
                links = responseValue.get('links')
                if links:
                    links_set.append(links)
        return links_set


    def create_transition_and_basic_places(self, petri_net, uri_login):
        place_req = Place("Req-"+uri_login, [])

        # creating transition
        transition = Transition(uri_login)

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


    def get_place_by_name(self, name):
        response = [x for x in self.petri_net.place() if x.name == name]
        if (response and len(response) > 0):
            return response[0]
        else:
            # se o place nao foi encontrado pelo metodo anterior, e possivel que o path tenha um
            # parametro
            response = [x for x in self.petri_net.place() if StringUtils.compare_uri_with_model(x.name, name)]
            if (response and len(response) > 0):
                return response[0]
        return None

    # def get_transition_by_name(self, petri_net, name):
    #     response = [x for x in petri_net.transition() if x.name == name]
    #     if (response and len(response) > 0):
    #         return response[0]
    #     else:
    #         # se o place nao foi encontrado pelo metodo anterior, e possivel que o path tenha um
    #         # parametro
    #         response = [x for x in petri_net.transition() if StringUtils.compare_uri_with_model(x.name, name)]
    #         if (response and len(response) > 0):
    #             return response[0]
    #     return None

    def get_transition_by_name(self, name):
        response = [x for x in self.petri_net.transition() if x.name == name]
        if (response and len(response) > 0):
            return response[0]
        else:
            # se o place nao foi encontrado pelo metodo anterior, e possivel que o path tenha um
            # parametro
            response = [x for x in self.petri_net.transition() if StringUtils.compare_uri_with_model(x.name, name)]
            if (response and len(response) > 0):
                return response[0]
        return None


    def create_name_to_req_place(self, uri):
        return f'Req-{uri}'

        

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



    def fill_input_places(self, log_json):
        for transition in self.petri_net.transition():
            if (StringUtils.compare_uri_with_model(transition.name, log_json.get('uri') )):
                # setting tokens related to RequestLine
                place_req_name='Req-'+log_json.get('uri')
                place = self.get_place_by_name(place_req_name)
                if place:
                    place.tokens.add(ColouredToken(LogUtils.create_request_line_from_log(log_json)))

                    # given a transistion, check if we have some input to set
                    # setting tokens related to requestBody
                    request_body_parameter_names = [*log_json.get('requestBody').keys()] # convert dict to array
                    transition = self.get_transition_by_name(log_json.get('uri'))
                    places = transition.input()
                    for parameter_name in request_body_parameter_names:
                        for place in places:
                            # se o place for output de alguma transição, nao devemos colocar tokens
                            if self.place_is_output(self.petri_net, place[0]):
                                continue
                            if place[0].name == parameter_name:
                                place[0].add(ColouredToken(LogUtils.create_data_from_request_body_in_log(log_json, parameter_name)))
                                break
                    # setting tokens related to parameters
        