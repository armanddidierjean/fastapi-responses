"""
Test Recursive infinite loop

In this test, fastapi-responses could enter an infinite loop trying to explore:
- `home`
    - `get_result`
        - `helper`
            - `get_result` again
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_responses import custom_openapi

app = FastAPI()

app.openapi = custom_openapi(app)


def helper(nb: int) -> str:
    return get_result(nb)


def get_result(nb: int = 1) -> str:
    if nb <= 0:
        return "Hello World!"
    return helper(nb - 1)


@app.get("/")
def home():
    return get_result(1)


client = TestClient(app)

openapi_schema = {
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/": {
            "get": {
                "summary": "Home",
                "operationId": "home__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        }
    },
}


def test_simple_app():
    res = client.get("/")
    assert res.status_code == 200

    res = client.get("/openapi.json/")
    print(res.json())
    assert res.json() == openapi_schema
