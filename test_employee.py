import pytest 
from unittest.mock import patch, MagicMock 
from main import app, get_db, Employee 
from fastapi.testclient import TestClient 
client = TestClient(app) 
@patch('main.get_db')
def test_create_employee(mock_db): 
    mock_cursor = MagicMock() 
    mock_conn = MagicMock() 
    mock_db.return_value = mock_conn 
    mock_conn.cursor.return_value = mock_cursor 
    mock_cursor.lastrowid = 1 
    response = client.post("/employees/", json={"name": "John", "position": "Dev", 
"salary": 50000}) 
    assert response.status_code == 200 
    assert response.json() == {"id": 1} 
@patch('main.get_db')
def test_read_employee(mock_db): 
    mock_cursor = MagicMock() 
    mock_conn = MagicMock() 
    mock_db.return_value = mock_conn 
    mock_conn.cursor.return_value = mock_cursor 
    mock_cursor.fetchone.return_value = (1, "John", "Dev", 50000) 
    response = client.get("/employees/1") 
    assert response.status_code == 200 
    assert response.json() == {"id": 1, "name": "John", "position": "Dev", "salary": 
50000} 