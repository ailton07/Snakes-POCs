import json

USER_IDENTIFICATION = 'user_id'
class ColouredToken:
    
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
        self.json_dict = json.dumps(value)
        self.user_id = value.get(USER_IDENTIFICATION)

    def __str__ (self) :
        return self.json_dict

    def __repr__ (self) :
        return self.__str__()

    def __eq__(self, other):
        if self.__str__() == other.__str__():
            return True
        return False

    def __hash__(self):
        return hash(self.json_dict)


class RequestResponseToken(ColouredToken):
    response_body = ''
    status_code = ''

    # def __init__ (self, json_dict, response) :
    #     self.response_body = json.dumps(response)
    #     super().__init__(json_dict)

    def __init__ (self, json_dict, response, status) :
        self.response_body = json.dumps(response)
        self.status_code = status
        super().__init__(json_dict)
        
    def get_response_body_dict (self):
        return json.loads(self.response_body)

    def get_status(self):
        response = {
            'status' : self.status_code,
            USER_IDENTIFICATION: self.user_id
        }
        return json.dumps(response)