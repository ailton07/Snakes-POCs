from utils.string_utils import StringUtils


class LogUtils:
    
    @staticmethod
    def create_data_from_request_body_in_log(log_json, parameter):
        return {
            parameter:log_json.get('requestBody').get(parameter),  
            'user_id':log_json.get('ip')
            }
        
    @staticmethod
    def create_request_line_from_log(log_json):
        return {
            'uri':log_json.get('uri'), 
            'method':log_json.get('method'), 
            'user_id':log_json.get('ip')
            }

    @staticmethod
    def create_response_status_from_log(log_json):
        return {
            'statusCode':log_json.get('statusCode'), 
            'user_id':log_json.get('ip')
            }

    @staticmethod
    def create_response_data_from_log(log_json, parameter):
        return {
            parameter:log_json.get('responseBody').get(parameter), 
            'user_id':log_json.get('ip')
            }    


    @staticmethod
    def create_request_response_from_log(log_json, openAPI2PetriNet=None):
        if openAPI2PetriNet == None:
            return {
                       'uri': log_json.get('uri'),
                       'method': log_json.get('method'),
                       'user_id': log_json.get('ip')
                   }, {
                       'response_body': log_json.get('responseBody'),
                       'user_id': log_json.get('ip')
                   }, log_json.get('statusCode')

        return {
                   'uri': StringUtils.get_open_api_url_from_url(openAPI2PetriNet, log_json.get('uri')),
                   'method': log_json.get('method'),
                   'user_id': log_json.get('ip')
               }, {
                   'response_body': log_json.get('responseBody'),
                   'user_id': log_json.get('ip')
               }, log_json.get('statusCode')