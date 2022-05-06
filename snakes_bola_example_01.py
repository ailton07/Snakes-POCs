import json
from ColouredToken import ColouredToken, RequestResponseToken
from prance import ResolvingParser
from OpenAPI2PetriNet import OpenAPI2PetriNet
from utils.log_utils import LogUtils
import snakes.plugins

snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

LOGS_PATH = 'logs/combined_bola_example.json'

OPENAPI_PATH = 'examples/BOLA_Example.yaml'
#OPENAPI_PATH = 'examples/link-example.yaml'
#OPENAPI_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example.yaml'

# Código utilizado na dissertação como exemplo
# loading log
logs_file = open(LOGS_PATH)
logs_json = json.load(logs_file)
logs_file.close()

def temp_create_link(petri_net, open_api_to_petri_parser):
    transitions = petri_net.transition()
    transition = transitions[0]

    # setting req arc
    place = open_api_to_petri_parser.get_place_by_name('Req-/accounts/{id}')
    petri_net.add_output(place.name, transition.name, Expression("request.get_next_request('/accounts/{id}', 'GET')"))
    # Value(ColouredToken(LogUtils.create_request_line_from_log('/accounts/{id}', 'GET', '')))
    # setting input1 arc
    place = open_api_to_petri_parser.get_place_by_name('id')
    petri_net.add_output(place.name, transition.name, Expression("request.get_object_from_response_body_dict().get('authentication').get('id')"))



def main():
    open_api_to_petri_parser = OpenAPI2PetriNet(OPENAPI_PATH)
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    transitions = petri_net.transition()
    import ipdb; ipdb.set_trace()
    petri_net.draw("value-0.png")
    # TODO: remove
    # uma vez que ainda não suportamos a criação automatica de links, a faremos manualmente aqui.
    # temp_create_link(petri_net, open_api_to_petri_parser)
    petri_net.draw("value-0.png")
    import ipdb; ipdb.set_trace()

    log_line = logs_json[1]
    #fill_input_places(petri_net, log_line)
    open_api_to_petri_parser.fill_input_places(log_line)
    petri_net.draw("value-0.png")
    

    request_line = RequestResponseToken(*LogUtils.create_request_response_from_log(log_line))
    email=ColouredToken(LogUtils.create_data_from_request_body_in_log(log_line, 'email'))
    password=ColouredToken(LogUtils.create_data_from_request_body_in_log(log_line, 'password'))
    authentication = ColouredToken(LogUtils.create_response_data_from_log(log_line, 'authentication'))

    import ipdb; ipdb.set_trace()
    #transition_1.fire(Substitution(request=request_line, email=email, password=password, status=response_status, authentication=authentication))
    transitions[0].fire(Substitution(request=request_line, email=email, password=password, authentication=authentication))
    petri_net.draw("value-1.png")
    
    log_line = logs_json[3]
    open_api_to_petri_parser.fill_input_places(log_line)
    petri_net.draw("value-0.png")

    import ipdb; ipdb.set_trace()
    request_line = RequestResponseToken(*LogUtils.create_request_response_from_log(log_line))
    id_variable = 6 # esse valor deve ser extraído do log
    transitions[1].fire(Substitution(request=request_line, id=id_variable ))

    
    petri_net.draw("value-0.png")


if __name__ == "__main__":
    main()
