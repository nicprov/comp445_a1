import socket
from urllib.parse import urlparse
from .http_method import HttpMethod
from .response import Response

BUFFER_SIZE = 1024
HTTP_VERSION = "1.0"
LINE_BREAK = "\r\n"


class Http:
    def __connect(self, host, port):
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__conn.connect((host, port))

    def __send(self, http_method, url, headers, body=None):
        # Extract path and domain
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        scheme = parsed_url.scheme
        path = parsed_url.path

        # Validate scheme
        if scheme == "http":
            port = 80
        else:
            raise Exception("Invalid scheme provided, must be http")

        # Validate host
        if host is None or not self.__validate_host(host):
            raise Exception("Invalid host provided")

        # Validate path
        if path == "":
            path = "/?" + parsed_url.query
        else:
            path += "?" + parsed_url.query

        # Connect to server
        self.__connect(host, port)

        # Add request method, path and http version
        if http_method == HttpMethod.GET:
            message = "GET {0} HTTP/{1}".format(path, HTTP_VERSION)
        else:
            message = "POST {0} HTTP/{1}".format(path, HTTP_VERSION)
        message += "{0}Host: {1}{2}".format(LINE_BREAK, host, LINE_BREAK)

        # Add headers
        if headers is not None:
            for header in headers:
                message += "{0}: {1}{2}".format(header[0], header[1], LINE_BREAK)

        # Add body
        if body is not None and http_method == HttpMethod.POST:
            message += "Content-Length: {0}{1}".format(len(body.encode()), LINE_BREAK)
            message += "{0}{1}{2}".format(LINE_BREAK, body, LINE_BREAK)

        # Add final line break
        message += LINE_BREAK
        self.__conn.send(message.encode())

    def __validate_host(self, host):
        try:
            socket.gethostbyname(host)
            return True
        except:
            return False

    def __get_response(self, http_method, url, headers, body=None):
        self.__send(http_method, url, headers, body)
        response = Response(self.__conn.recv(BUFFER_SIZE).decode().split(LINE_BREAK))
        if response.get_status_code() in [301, 302]: # Temporary or permanent redirect
            location = response.get_header("location")
            if location is None:
                location = response.get_header("Location")
            parsed_url = urlparse(url)
            new_url = "{0}://{1}{2}?{3}".format(parsed_url.scheme, parsed_url.hostname, location, parsed_url.query)
            return self.__get_response(http_method, new_url, headers, body)
        else:
            return response

    def get(self, url, headers=None):
        return self.__get_response(HttpMethod.GET, url, headers)

    def post(self, url, headers=None, body=None):
        return self.__get_response(HttpMethod.POST, url, headers, body)
