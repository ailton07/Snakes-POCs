class StringUtils:
    # return true if the URIs are the same
    # ex: "/rest/basket/6" and "/rest/basket/{basketId}"
    @staticmethod
    def compare_uri_with_model(model_uri, uri):
        if model_uri.split(' '):
            model_uri = model_uri.split(' ')[0]
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


    @staticmethod
    def get_open_api_url_from_url(openAPI2PetriNet, uri):
        list_of_paths = list(openAPI2PetriNet.parser.specification.get('paths').keys())
        for open_api_path in list_of_paths:
            if StringUtils.compare_uri_with_model(open_api_path, uri):
                return open_api_path
        return None


    @staticmethod
    def get_first_diff_in_uri(model_uri, uri):
        model_uri_splited = model_uri.split('/')
        uri_splited = uri.split('/')
        if (len(model_uri_splited) == len(uri_splited)):
            for i in range(len(model_uri_splited)):
                if (model_uri_splited[i] != uri_splited[i]):
                    if ('{' in model_uri_splited[i]):
                        return uri_splited[i]
        else:
            return None

        return None