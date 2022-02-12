class Response:
    def __init__(self, raw):
        self.__raw = raw

    def formatted(self):
        response = ""
        for line in self.__raw:
            if line == "":
                response += "\n"
            else:
                response += line + "\n"
        return response

    def get_status_code(self):
        return self.__raw[0].split(" ")[1]

    def get_header(self, header):
        for line in self.__raw:
            if line == "":
                return None
            else:
                parsed_header = line.split(":")
                if parsed_header[0] == header:
                    return parsed_header[1]
        return None
