from fastapi.testclient import TestClient
import pytest
import httpx

from Backend.microservices.app.API.v1.server_fastapi import app

client: function = TestClient(app)

def test