import pytest
from fastapi.testclient import TestClient

from Backend.microservices.app.CryptoAPI.v1.server_fastapi import app


client: function = TestClient(app)
