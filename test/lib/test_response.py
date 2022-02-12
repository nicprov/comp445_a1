from src.lib.http import Http


def test_get_body():
    response = Http().get("http://httpbin.org/status/418")
    assert response.get_body() == '\n' \
                                  '    -=[ teapot ]=-\n' \
                                  '\n' \
                                  '       _...._\n' \
                                  "     .'  _ _ `.\n" \
                                  '    | ."` ^ `". _,\n' \
                                  '    \\_;`"---"`|//\n' \
                                  '      |       ;/\n' \
                                  '      \\_     _/\n' \
                                  '        `"""`\n'


def test_get_status():
    response = Http().get("http://httpbin.org/status/200")
    assert response.get_status() == "OK"


def test_get_status_code():
    response = Http().get("http://httpbin.org/status/400")
    assert response.get_status_code() == 400


def test_get_header():
    response = Http().get("http://httpbin.org/status/500")
    assert response.get_header("Connection") == "close"
