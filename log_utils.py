
class LogUtils:
    
    @staticmethod
    def create_data_from_log(log_json, parameter):
        return {
            parameter:log_json.get('requestBody').get(parameter),  
            'id':log_json.get('ip')
            }
        
    @staticmethod
    def create_request_line_from_log(log_json):
        return {
            'uri':log_json.get('uri'), 
            'method':log_json.get('method'), 
            'id':log_json.get('ip')
            }

    @staticmethod
    def create_response_status_from_log(log_json):
        return {
            'statusCode':log_json.get('statusCode'), 
            'id':log_json.get('ip')
            }

    @staticmethod
    def create_response_data_from_log(log_json, parameter):
        return {
            parameter:log_json.get('responseBody').get(parameter), 
            'id':log_json.get('ip')
            }    
 