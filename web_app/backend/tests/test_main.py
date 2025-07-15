from fastapi.testclient import TestClient
from web_app.backend.main import app
from unittest.mock import patch, MagicMock
import datetime

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

@patch('web_app.backend.main.list_strategies')
def test_get_strategies(mock_list_strategies):
    mock_list_strategies.return_value = [{"id": 1, "name": "test", "rule_ids": [1, 2]}]
    response = client.get("/strategies")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "test", "rule_ids": [1, 2]}]

@patch('web_app.backend.main.cm.context')
def test_get_prices(mock_context):
    mock_conn = mock_context.return_value.__enter__.return_value
    mock_cur = mock_conn.cursor.return_value
    mock_cur.fetchall.return_value = [(datetime.date(2022, 1, 1), 100, 110, 90, 105)]
    response = client.get("/prices/AAPL")
    assert response.status_code == 200
    assert response.json() == [{"time": "2022-01-01", "open": 100, "high": 110, "low": 90, "close": 105}]

def test_chat():
    response = client.post("/chatbot?question=test")
    assert response.status_code == 200
    assert response.json() == {"answer": "This feature is not available yet."}
