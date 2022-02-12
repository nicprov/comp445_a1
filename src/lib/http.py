import socket
from src.lib.http_method import HttpMethod
from src.lib.response import Response

BUFFER_SIZE = 1024
LINE_BREAK = "\r\n"


class Http:
    def __init__(self, host, port=80):
        self.__headers = []
        self.__body = ""
        self.__host = host
        self.__port = port

        # Establish TCP connection
        self.__connect()

    def __connect(self):
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__conn.connect((self.__host, self.__port))

    def __send(self, httpMethod, path):
        # Add request method, path and http version
        if httpMethod == HttpMethod.GET:
            message = "GET {0} HTTP/1.0".format(path)
        else:
            message = "POST {0} HTTP/1.0".format(path)
        message += "{0}Host: {1}{2}".format(LINE_BREAK, self.__host, LINE_BREAK)

        # Add headers
        for header in self.__headers:
            message += "{0}: {1}{2}".format(header[0], header[1], LINE_BREAK)

        # Add body
        if self.__body != "" and httpMethod == HttpMethod.POST:
            message += "{0}{1}".format(self.__body, LINE_BREAK)

        # Add final line break
        message += LINE_BREAK
        self.__conn.send(message.encode())

    def get(self, path, headers=None):
        if headers is None:
            headers = []
        self.__headers = headers
        self.__send(HttpMethod.GET, path)
        return Response(self.__conn.recv(BUFFER_SIZE).decode().split(LINE_BREAK))

    def post(self, path, headers=None, body=""):
        if headers is None:
            headers = []
        self.__headers = headers
        self.__body = body
        self.__send(HttpMethod.POST, path)
        return Response(self.__conn.recv(BUFFER_SIZE).decode().split(LINE_BREAK))
