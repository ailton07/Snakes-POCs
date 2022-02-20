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

# loading OpenAPI
# Convert YAML to JSON https://www.convertjson.com/yaml-to-json.htm
# with open('examples/JuiceShop.json', 'r') as spec_file:
#    spec_dict = json.load(spec_file)
# spec = create_spec(spec_dict)

#parser = ResolvingParser('examples/JuiceShop.yaml')


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
    open_api_to_petri_parser = OpenAPI2PetriNet('examples/JuiceShop.yaml')

    import ipdb; ipdb.set_trace()
    
    petri_net = open_api_to_petri_parser.create_petri_net()
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
