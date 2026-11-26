from assistant.app import app


def test_chat_endpoint():
    client = app.test_client()
    r = client.post("/chat", json={"message": "what is elliott wave"})
    assert r.status_code == 200 and r.get_json()["intent"] == "elliott_wave"


def test_chat_rejects_empty():
    assert app.test_client().post("/chat", json={"message": "  "}).status_code == 400
    assert app.test_client().post("/chat", data="not json").status_code == 400


def test_index_page():
    assert app.test_client().get("/").status_code == 200
