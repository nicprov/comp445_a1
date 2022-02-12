from src.lib.http import Http

def test_get():
    http = Http("httpbin.org")
    print(http.get("/status/418").formatted())

def test_post():
    return 1