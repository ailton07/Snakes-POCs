import json
from coloured_token import ColouredToken
from numpy import place
from log_utils import LogUtils
import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *


# Instruções no livro Web Scraping com Pyhton
# source venv/bin/activate

# loading log
logs_file = open('logs/combined_login.json')
logs_json = json.load(logs_file)
logs_file.close()

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
    petri_net.add_output(place_status.name, transition.name, Variable("status"))

    return transition


def create_petri_net():
    # constants
    uri_login =  "/rest/user/login"

    petri_net = PetriNet('Juice Shop')
    
    # transition 1
    # creating basic structure
    transition_1 = create_transition_and_basic_places(petri_net, uri_login)

    # creating inputs to the transition 1
    place_input_email = Place("email", [])
    place_input_password = Place("password", [])

    # creating outputs to the transition 1
    place_output_authentication = Place("authentication", [])
    place_input_output_bid = Place("bid", [])

    # conecting places to the transtion 1
    petri_net.add_place(place_input_email)
    petri_net.add_place(place_input_password)
    petri_net.add_place(place_output_authentication)
    petri_net.add_place(place_input_output_bid)

    petri_net.add_input(place_input_email.name, transition_1.name, Variable("email"))
    petri_net.add_input(place_input_password.name, transition_1.name, Variable("password"))
    petri_net.add_output(place_output_authentication.name, transition_1.name, Variable("authentication"))
    petri_net.add_output(place_input_output_bid.name, transition_1.name, Expression("authentication.get_element_from_dict('bid')"))

    # transition 2
    uri_login =  "/rest/basket/{basketId}"
    transition_2 = create_transition_and_basic_places(petri_net, uri_login)
    petri_net.add_input(place_input_output_bid.name, transition_2.name, Variable("email"))

    return petri_net, transition_1

# return true if the URIs are the same
# ex: "/rest/basket/6" and "/rest/basket/{basketId}"
def compare_uri_with_model(model_uri, uri):
    model_uri_splited = model_uri.split('/')
    uri_splited = uri.split('/')
    if (len(model_uri_splited) == len(uri_splited)):
        for i in range(len(model_uri_splited)):
            if (model_uri_splited[i] != uri_splited[i]):
                if not ('{' in model_uri_splited[i]):
                    return False
    else:
        return False


    return True


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
                    place[0].add(ColouredToken(LogUtils.create_data_from_log(log_json, parameter_name)))
                    continue
    else:
        for transition in petri_net.transition():
            if (compare_uri_with_model(transition.name, log_json.get('uri') )):
                place_req_name='Req-'+transition.name
                place = get_place_by_name(petri_net, place_req_name)
                place.tokens.add(ColouredToken(LogUtils.create_request_line_from_log(log_json)))
    



def main():
    petri_net, transition_1 = create_petri_net()
    petri_net.draw("value-0.png")
    
    #for log_json in logs_json:
    #    fill_input_places(petri_net, log_json)
    log_line = logs_json[1]
    fill_input_places(petri_net, log_line)
    #fill_input_places(petri_net, logs_json[3])

    petri_net.draw("value-0.png")

    request_line = ColouredToken(LogUtils.create_request_line_from_log(log_line))
    response_status = ColouredToken(LogUtils.create_response_status_from_log(log_line))
    email=ColouredToken(LogUtils.create_data_from_log(log_line, 'email'))
    password=ColouredToken(LogUtils.create_data_from_log(log_line, 'password'))
    authentication = ColouredToken(LogUtils.create_response_data_from_log(log_line, 'authentication'))

    import ipdb; ipdb.set_trace()

    transition_1.fire(Substitution(request=request_line, email=email, password=password, status=response_status, authentication=authentication))
    petri_net.draw("value-0.png")


if __name__ == "__main__":
    main()
