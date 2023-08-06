"""
    HTTP features for HTTP based backends and requests 
"""

import requests
import ssl
import pathlib
from pydeen.types import Request, Connector, Result, Backend, Auth

class HTTPRequest(Request):

    def __init__(self, connector: Connector) -> None:
        super().__init__()
        self.headers = {
            'user-agent': 'python-request (pydeen)'
        }
        self.connector = connector
        self.http_request = None
        self.params  = {}
        self.result  = None
        self.url:str = None
        self.status_code:int = 0
        self.status_text:str = ""
        self.payload:str = None
        self.response:str = None

    def get_params(self):
        params = {}
        backend_params = self.connector.get_backend().get_params()
        if len(backend_params) > 0:
            params += backend_params        
        
        if len(self.connector.params) > 0:
            params += self.connector.params

        if len(self.params) > 0:
            params += self.params
        return params

    def get_response_text(self) -> str:
        if self.http_request != None:
            return self.http_request.text
        else: 
            return None    

    def get_response_json(self):
        return self.http_request.json()

    def is_response_availabe(self) -> bool:
        if self.http_request == None:
            return False
        else:
            return True 


    def get_status_code(self) -> int:
        return self.status_code

    def set_result_from_request(self):
        # check http result is given
        self.result = None
        if self.http_request == None:
            self.status_code = 500
            self.status_text = "unknown"            
            return None
        
        # set status code and reason
        self.status_code = self.http_request.status_code
        self.status_text = self.http_request.reason

        # check result type
        self.response = self.http_request.text
        try:    
            result = self.http_request.json()
        except:
            result = self.response
            self.trace("request result is no json. set text")

        # set result object
        if result != None:
            self.result = Result(result)
        return self.result         

    def get(self, path_append="", parameters:dict=None) -> int:
        url = self.connector.build_url(path_append, parameters)
        auth = self.connector.get_backend().get_auth_info().get_auth_for_request()
        params = self.get_params()
        self.trace(f"URL: {url}, params = {params}")

        self.url = url
        self.payload = None
        
        self.http_request = requests.get(url, params=params, headers=self.headers, auth=auth)
        self.set_result_from_request()
        if self.http_request == None:
            self.error(f"request get failed: URL {url}")
        
        self.trace(f"request get result: {self.status_code}")    
        return self.status_code

    def post(self, payload:str=None, path_append="", parameters:dict=None) -> int:
        url = self.connector.build_url(path_append, parameters)
        auth = self.connector.get_backend().get_auth_info().get_auth_for_request()
        params = self.get_params()
        self.trace(f"URL: {url}, params = {params}")
        
        self.url = url
        if payload != None: 
            self.payload  = payload
        else:
            self.trace("use loaded payload for post request")    

        self.http_request = requests.post(url, self.payload, params=params, headers=self.headers, auth=auth)
        self.set_result_from_request()    
        if self.http_request == None:
            self.error(f"request get failed: URL {url}")
        
        self.trace(f"request get result: {self.status_code}")    
        return self.status_code

    def load_payload(self, filename:str) -> bool:
        try:
           self.payload = None
           self.payload = pathlib.Path(filename).read_text()
           if self.payload != None:
            self.trace(f"request payload loaded from file {filename}")
            return True
           else:
            self.error(f"Error while loading payload from file {filename}")
            return False 
        except Exception as exc:
            self.error(f"Error while loading payload: {type(exc)} - {exc}")
            return False

class HTTPBackend(Backend):

    def __init__(self, name:str, url:str, auth:Auth=None):
        super().__init__(name, auth)
        self.type = "pydeen.HTTPBackend"
        self.set_property(Backend.BACKEND_PROP_URL, url)
        self.ssl_verify_mode:ssl.VerifyMode=None

    def get_ssl_verify_mode(self) -> ssl.VerifyMode:
        return self.ssl_verify_mode

    def set_ssl_verify_mode(self, ssl_verify_mode:ssl.VerifyMode):
        self.ssl_verify_mode = ssl_verify_mode
        self.trace(f"SSL Verify mode set to: {self.ssl_verify_mode}")    


    def set_ssl_verify_mode_none(self):
        self.ssl_verify_mode = ssl.CERT_NONE
        self.trace("SSL Verify mode deactivated")    

    def set_ssl_verify_mode_client_with_pem(self, path_to_pem:str, ssl_method:ssl._SSLMethod=ssl.PROTOCOL_TLS_CLIENT) -> bool:
        try:
            ssl_context = ssl.SSLContext(ssl_method)
            pem_file = pathlib.Path(path_to_pem)
            ssl_context.load_verify_locations(cafile=pem_file)
            self.set_ssl_verify_mode(ssl_context)
            return True               
        except Exception as exc:
            self.error(f"Error while setting SSL context: {type(exc)} - {exc}")    
            return False

    def set_ssl_verify_mode_ignore_all(self, protocol:ssl._SSLMethod=None) -> bool:
        ssl_context = ssl.SSLContext(protocol=protocol)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return True

class HTTPConnector(Connector):
    """
        Connector for HTTP Calls
    """
    def __init__(self, backend:Backend=None, url_or_endpoint:str="") -> None:
            
            # check backend 
            if backend == None:
                raise Exception("HTTP Connector via url not implemented yet")
                self.endpoint = ""    
                # if url_or_endpoint == "" or url_or_endpoint.find("://") < 1:
                #     raise Exception("invalid URL if no backend is given") 
                
                # split_protocol = url.split("://")
                # protocol = split_protocol[0]
                # rest_protocol = split_protocol[1]

                # pos_path = rest_protocol.find("/")
                # if pos_path > 0:
                #     hostname = rest_protocol.left(pos_path)
                #     path = rest_protocol.
            else:
                self.endpoint = url_or_endpoint
    
            Connector.__init__(self, backend)
            self.type = "pydeen.HTTPConnector"

            # remember last request
            self.last_request_code:int = 0
            self.last_request_status:str = None
            self.last_request_url:str = None
            self.last_request_payload:any =None
            self.last_request_response:any =None

            
    def path_append(self, path, append) -> str:
        if append == "" or append == None:
            return path
        if path == "":
            return append
        if path[-1] == "/" or append[0] == "/":
            return path + append
        else:
            return path + "/" + append

    def build_url(self, path_append, parameters:dict=None) -> str:
        # check url is given by backend or parameter
        if path_append.find("://") > 0:
            url = path_append
        else:     
            url = self.get_backend().get_property(Backend.BACKEND_PROP_URL)
        
        # no: build via backend fragments    
        if url == None or url == "":
            result = self.get_backend().get_property(Backend.BACKEND_PROP_PROTOCOL) + "://"
            result += self.get_backend().get_property(Backend.BACKEND_PROP_HOST)
            port = self.get_backend().get_property(Backend.BACKEND_PROP_PORT)
            if port != None and port != "":
                result += ":" + port
        
            result = self.path_append(result, self.get_backend().get_property(Backend.BACKEND_PROP_PATH))
            result = self.path_append(result, self.endpoint)
            result = self.path_append(result, path_append)
        else:
        # yes: use this without further fragments except append info    
            if url != path_append:
                result = self.path_append(url, path_append)
            else:
                result = url

        # check for parameters
        if parameters != None:
            self.trace("build url with parameters detected")
            url_params = ''
            for name in parameters.keys():
                sep = "="
                if name == "$filter":
                    value = str(parameters[name]).lower()
                    if value.find("contains") >= 0:
                        self.trace(f"OData filter exception found for {value}")
                        sep = " "

                url_param = name + sep + parameters[name]
                if url_params == '':
                    url_params = url_param
                else:
                    url_params += '&' + url_param

            if result.find("?") < 0:
                result += "?" + url_params
            else:
                parts = result.split("?")
                result = parts[0] + '?' + parts[1] + '&' + url_params


        print("URL:", result)
        return result

    def create_request(self) -> HTTPRequest:
        request = HTTPRequest(self)   
        request.debug = self.debug   # forward debug mode 
        request.interactive = self.interactive
        return request   

    def set_last_request(self, code:int=0, status:str=None, response:any=None, payload:any=None, url:str=None):
        """set the last request information to the connector object for debug issues

        :param code: _description_, defaults to 0
        :type code: int, optional
        :param status: _description_, defaults to None
        :type status: str, optional
        :param response: _description_, defaults to None
        :type response: Any, optional
        :param payload: _description_, defaults to None
        :type payload: Any, optional
        :param url: _description_, defaults to None
        :type url: str, optional
        """
    
        self.last_request_url = url
        self.last_request_code = code
        self.last_request_status = status
        self.last_request_payload = payload
        self.last_request_response = response

    def set_last_request_from_object(self, request:HTTPRequest):
        """set last request infos from HTTPRequest object

        :param request: _description_
        :type request: HTTPRequest
        """
        self.set_last_request(url=request.url, code=request.status_code, status=request.status_text, response=request.response, payload=request.payload)

    def reset_last_request(self):
        """reset last request info
        """
        self.set_last_request()

    def get_last_request_code(self) -> int:
        """get the code of last request

        :return: _description_
        :rtype: int
        """
        return self.last_request_code

    def get_last_request_status(self) -> str:
        """get the status of last request

        :return: _description_
        :rtype: str
        """
        return self.last_request_status

    def get_last_request_url(self) -> str:
        """get the url of last request

        :return: _description_
        :rtype: str
        """
        return self.last_request_url

    def get_last_request_payload(self) -> any:
        """get the payload of last request

        :return: _description_
        :rtype: any
        """
        return self.last_request_payload
    
    def get_last_request_response(self) -> any:
        """get the response of last request

        :return: _description_
        :rtype: any
        """
        return self.last_request_response
    