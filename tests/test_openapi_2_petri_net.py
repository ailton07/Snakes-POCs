import json, pytest
from OpenAPI2PetriNet import OpenAPI2PetriNet


@pytest.fixture
def get_logs_json():
    # loading log
    logs_file = open('logs/combined_login_test.json')
    logs_json = json.load(logs_file)
    logs_file.close()
    return logs_json


@pytest.fixture
def get_juice_shop_petri_net():
    open_api_to_petri_parser = OpenAPI2PetriNet('specification/JuiceShop.yaml')
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    return open_api_to_petri_parser, petri_net


def test_fill_input_places(get_juice_shop_petri_net, get_logs_json):
    # given
    open_api_to_petri_parser, petri_net = get_juice_shop_petri_net
    log_line = get_logs_json[1]
    
    # when we call fill_input_places to the log line
    open_api_to_petri_parser.fill_input_places(log_line)
    
    # then, check if the places have tokens related to requestBody

    # check all places
    places_with_tokens = 0
    for place in [x for x in petri_net.place()]:
        places_with_tokens = places_with_tokens + place.tokens.size()

    # we should have 3 tokens, one to the requestLine and two to the requestBodies
    assert places_with_tokens == 3

    # check only the requestBodies inputs
    # extract the names of requestBodies
    request_body_parameter_names = [*log_line.get('requestBody').keys()] # convert dict to array
    places_with_tokens = 0
    for request_body_parameter_name in [x.name for x in petri_net.place()]:
        if (request_body_parameter_name in request_body_parameter_names):
            place = open_api_to_petri_parser.get_place_by_name(request_body_parameter_name)
            assert place.tokens.size() == 1
            print (f'place(name={place.name} has 1 token)')
            places_with_tokens = places_with_tokens + 1
    assert places_with_tokens == 2
