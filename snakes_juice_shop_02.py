import json
from ColouredToken import ColouredToken, RequestResponseToken
from prance import ResolvingParser
from OpenAPI2PetriNet import OpenAPI2PetriNet
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


def main():
    import ipdb; ipdb.set_trace()
    
    open_api_to_petri_parser = OpenAPI2PetriNet('examples/JuiceShop.yaml')
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    transitions = petri_net.transition()
    petri_net.draw("value-0.png")

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
    
    
    
    petri_net.draw("value-0.png")


if __name__ == "__main__":
    main()
