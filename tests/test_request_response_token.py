import pytest, json
from ColouredToken import RequestResponseToken
from utils.log_utils import LogUtils

logs_file = open('tests/logs/combined_login_test.json')
logs_json = json.load(logs_file)
logs_file.close()

def test_request_response_token():
    # given a request described in logs_json[1]
    log_line = logs_json[1]
    request_line = LogUtils.create_request_line_from_log(log_line)
    response_body = log_line.get('responseBody')

    # when we create a RequestResponseToken
    token = RequestResponseToken(request_line, response_body)

    # we can assert the behaviors
    assert token.get_dict() == request_line
    assert token.get_response_body_dict() == response_body
    
    