import json
from ColouredToken import ColouredToken, RequestResponseToken
from prance import ResolvingParser
from OpenAPI2PetriNet import OpenAPI2PetriNet
from utils.log_utils import LogUtils
from utils.string_utils import StringUtils
import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

# Código utilizado na dissertação como exemplo
# loading log
logs_file = open('logs/combined_bola_example.json')
logs_json = json.load(logs_file)
logs_file.close()

def temp_create_link(petri_net, open_api_to_petri_parser):
    transitions = petri_net.transition()
    transition = transitions[0]
    place = open_api_to_petri_parser.get_place_by_name(petri_net, 'id')
    petri_net.add_output(place.name, transition.name, Expression("request.get_object_from_response_body_dict().get('authentication').get('id')"))



def main():
    open_api_to_petri_parser = OpenAPI2PetriNet('examples/BOLA_Example.yaml')
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    transitions = petri_net.transition()
    import ipdb; ipdb.set_trace()
    petri_net.draw("value-0.png")
    # uma vez que ainda não suportamos a criação automatica de links, a faremos manualmente aqui.
    temp_create_link(petri_net, open_api_to_petri_parser)
    petri_net.draw("value-0.png")
    import ipdb; ipdb.set_trace()

    log_line = logs_json[1]
    #fill_input_places(petri_net, log_line)
    open_api_to_petri_parser.fill_input_places(petri_net, log_line)
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
    open_api_to_petri_parser.fill_input_places(petri_net, log_line)
    petri_net.draw("value-0.png")

    import ipdb; ipdb.set_trace()
    request_line = RequestResponseToken(*LogUtils.create_request_response_from_log(log_line))
    id_variable = 6 # esse valor deve ser extraído do log
    transitions[1].fire(Substitution(request=request_line, id=id_variable ))

    
    petri_net.draw("value-0.png")


if __name__ == "__main__":
    main()
