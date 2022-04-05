import json

USER_IDENTIFICATION = 'user_id'
class ColouredToken:
    json_dict = None
    user_id = None
    
    def get_dict (self):
        return json.loads(self.json_dict)

    def check_if_contains_attribute(self, object, element):
        #import ipdb; ipdb.set_trace()
        for (key, value) in object.items():
            if key == element:
                return str(value)
            elif isinstance(value, dict):
                return self.check_if_contains_attribute(value, element)
            
        return None


    def get_element_from_dict (self, element):
        result = self.check_if_contains_attribute(self.get_dict(), element)
        if result:
            response = {
                element : self.check_if_contains_attribute(self.get_dict(), element),
                USER_IDENTIFICATION: self.user_id
                }

            return json.dumps(response)


    def __init__ (self, value) :
        self.json_dict = json.dumps(value, separators=(',\n', ':'))
        self.user_id = value.get(USER_IDENTIFICATION)

    def __str__ (self) :
        return self.json_dict

    def __repr__ (self) :
        return self.__str__() if len(self.__str__()) < 60 else self.__str__()[0:60:1]+'...'

    def __eq__(self, other):
        if self.__str__() == other.__str__():
            return True
        return False

    def __hash__(self):
        return hash(self.json_dict)


class RequestResponseToken(ColouredToken):
    # request data
    uri = None
    method = None
    # user_id is in ColouredToken
    # response data
    response_body = None
    status_code = None

    # def __init__ (self, json_dict, response) :
    #     self.response_body = json.dumps(response)
    #     super().__init__(json_dict)

    def __init__ (self, json_dict, response, status) :
        self.response_body = json.dumps(response, separators=(',\n', ':'))
        self.status_code = status
        self.uri = json_dict.get('uri')
        self.method = json_dict.get('method')
        super().__init__(json_dict)
        
    def get_response_body_dict (self):
        return json.loads(self.response_body)

    def get_object_from_response_body_dict (self):
        return json.loads(self.response_body).get('response_body')

    def get_status(self):
        response = {
            'status' : self.status_code,
            USER_IDENTIFICATION: self.user_id
        }
        return json.dumps(response, separators=(',\n', ':'))

    def get_response(self):
        body = json.loads(self.response_body)
        return json.dumps(body.get('response_body'), separators=(',\n', ':'))

    def _create_request_line(self, uri_str, method_str, ip_str):
        return ColouredToken({
            'uri': uri_str,
            'method': method_str,
            'user_id': ip_str
        })

    def get_next_request(self, uri_str, method_str):
        if self.uri is None:
            raise Exception("This token don't have request information")
        next_request = self._create_request_line(uri_str, method_str, self.user_id)
        return next_request