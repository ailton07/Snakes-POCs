import json, pytest
from unittest import mock
import snakes
from unittest.mock import Mock

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


@pytest.fixture
def get_juice_shop_petri_net_without_links():
    open_api_to_petri_parser = OpenAPI2PetriNet('specification/JuiceShop.yaml')
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop', create_links=False)
    return open_api_to_petri_parser, petri_net


def test_create_petri_net_with_links(get_juice_shop_petri_net):
    # given the JuiceShop OpenApi specification
    # when we create a petri net with links
    open_api_to_petri_parser, petri_net = get_juice_shop_petri_net

    # then, we should have only 11 arcs
    assert petri_net
    quantity_of_arcs = 0
    for transition in petri_net.transition():
        quantity_of_arcs = quantity_of_arcs + len(transition.input())
        quantity_of_arcs = quantity_of_arcs + len(transition.output())
    assert quantity_of_arcs == 11

    # and we should have the link arc as transition 1 output
    assert 'Req-/rest/basket/{bid}' in [arc[0].name for arc in petri_net.transition()[0].output()]
    #assert 'bid' in [arc[0].name for arc in petri_net.transition()[0].output()]


def test_create_petri_net_excluding_links(get_juice_shop_petri_net_without_links):
    # given the JuiceShop OpenApi specification
    # when we create a petri net excluding links
    open_api_to_petri_parser, petri_net = get_juice_shop_petri_net_without_links

    # then, we should have only 9 arcs
    quantity_of_arcs = 0
    for transition in petri_net.transition():
        quantity_of_arcs = quantity_of_arcs + len(transition.input())
        quantity_of_arcs = quantity_of_arcs + len(transition.output())
    assert quantity_of_arcs == 9

    # and we should not have the link arc
    for arc in petri_net.transition()[0].output():
        assert arc[0].name != 'Req-/rest/basket/{bid}'
        assert arc[0].name != 'bid'


def test_create_link_arcs(get_juice_shop_petri_net_without_links):
    # given petri net without links
    open_api_to_petri_parser, petri_net_excluding_links = get_juice_shop_petri_net_without_links

    # when we call the create_link_arcs method
    with mock.patch.object(petri_net_excluding_links, 'add_output', wraps=petri_net_excluding_links.add_output) as fake_add_output:
        open_api_to_petri_parser.create_link_arcs()

    # then we have the invocation of add_output to add a new arc
    assert fake_add_output.call_count == 2
    # and we have 10 arcs in the petri net
    quantity_of_arcs = 0
    for transition in petri_net_excluding_links.transition():
        quantity_of_arcs = quantity_of_arcs + len(transition.input())
        quantity_of_arcs = quantity_of_arcs + len(transition.output())
    assert quantity_of_arcs == 10


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
        request_body_parameter_name_splited = request_body_parameter_name.split()[0] if len(request_body_parameter_name.split()) > 0 else request_body_parameter_name
        if (request_body_parameter_name_splited in request_body_parameter_names):
            place = open_api_to_petri_parser.get_place_by_name(request_body_parameter_name)
            assert place.tokens.size() == 1
            print (f'place(name={place.name} has 1 token)')
            places_with_tokens = places_with_tokens + 1
    assert places_with_tokens == 2
