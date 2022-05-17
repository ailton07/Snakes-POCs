import pytest, json
from utils.string_utils import StringUtils

from OpenAPI2PetriNet import OpenAPI2PetriNet

@pytest.fixture
def get_juice_shop_petri_net():
    open_api_to_petri_parser = OpenAPI2PetriNet('specification/JuiceShop.yaml')
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    return open_api_to_petri_parser, petri_net

def test_get_open_api_url_from_url(get_juice_shop_petri_net):
    # given the JuiceShop OpenApi specification
    # when we create a petri net with links
    open_api_to_petri_parser, petri_net = get_juice_shop_petri_net
    uri = '/rest/basket/6'
    expected_uri = '/rest/basket/{bid}'

    # when we try to extract a normalized url from a concrete url
    uri_extracted = StringUtils.get_open_api_url_from_url(open_api_to_petri_parser, uri)

    # we extract a normalized url
    assert uri_extracted == expected_uri
