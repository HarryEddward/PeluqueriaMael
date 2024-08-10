import pytest
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import TextModel, encrypt, decrypt
from pydantic import ValidationError
from termcolor import cprint

# Pruebas para la validación de texto

def test_valid_ascii_text():
    assert TextModel(text='Hello World') == TextModel(text='Hello World')

def test_invalid_ascii_text():
    with pytest.raises(ValidationError):
        TextModel(text='Hello\x00World')

def test_valid_text_with_permitted_characters():
    assert TextModel(text='Hello, World!') == TextModel(text='Hello, World!')

def test_invalid_text_with_special_characters():
    with pytest.raises(ValidationError):
        TextModel(text='Hello @#%')

def test_invalid_utf8_text():
    with pytest.raises(ValidationError):
        TextModel(text='Café')

# Mock para la lógica de encriptación y desencriptación

def test_encrypt():
    # Simulación del comportamiento esperado para pruebas
    mock_text = 'Hello World'
    result = encrypt(mock_text)
    assert isinstance(result, bytes)  # Verificar que el resultado es de tipo bytes

def test_decrypt():
    # Simulación del comportamiento esperado para pruebas
    encrypted_text = encrypt('Hello World')
    print("\n")
    cprint(encrypted_text, "green", "on_black")
    result = decrypt(encrypted_text)
    cprint(result, "green", "on_black")
    print("\n")
    assert isinstance(result, bytes)  # Verificar que el resultado es de tipo bytes
    assert result == b'Hello World'

