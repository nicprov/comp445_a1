import pytest
from src.lib.http import Http


def test_get_success():
    response = Http().get("http://httpbin.org/status/200")
    assert response.get_status_code() == 200


def test_url_invalid_path():
    response = Http().get("http://httpbin.org")
    assert response.get_status_code() == 200


def test_url_invalid_scheme():
    with pytest.raises(Exception):
        Http().get("ftp://httpbin.org")


def test_url_empty_host():
    with pytest.raises(Exception):
        Http().get("http://")


def test_url_invalid_host():
    with pytest.raises(Exception):
        Http().get("http://httpbin")


def test_get_redirect_301():
    response = Http().get("http://httpbin.org/status/301")
    assert response.get_status_code() == 404


def test_get_redirect_302():
    response = Http().get("http://httpbin.org/status/302")
    assert response.get_status_code() == 404

def test_post_no_body_success():
    response = Http().post("http://httpbin.org/post", [("Content-Type", "application/json")])
    assert response.get_status_code() == 200


def test_post_body_success():
    response = Http().post("http://httpbin.org/post", [("Content-Type", "application/json")], '{"Assignment":1}')
    assert response.get_status_code() == 200
